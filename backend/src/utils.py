from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import asyncio
from src.dependencies import get_db
from src.rasp.models import Rasp, Device
from src.history.service import HistoryService
from src.websockets import WebSocketMessageHandler
from src.config import global_config
from src.users.models import UserRaspLink, UserDeviceLink

history = HistoryService()
websocket_handler = WebSocketMessageHandler()

async def check_alive_status():
    while True:
        await asyncio.sleep(30)  
        db_session = next(get_db())

        try:
            now = datetime.utcnow()
            time_span = now - timedelta(seconds=global_config.DEVICE_STATUS_EXPIRE_SECONDS)

            dead_rasps = db_session.query(Rasp).filter(Rasp.last_update < time_span, Rasp.status == "online").all()
            dead_devices = db_session.query(Device).filter(Device.last_update < time_span, Device.status == "online").all()

            for rasp in dead_rasps:
                rasp.status = "offline"
            for device in dead_devices:
                device.status = "offline"
            
            dead_rasp_ids = [rasp.id for rasp in dead_rasps]
            dead_device_ids = [device.id for device in dead_devices]

            deleted_rasp_links = db_session.query(UserRaspLink).filter(UserRaspLink.rasp_id.in_(dead_rasp_ids)).delete(synchronize_session=False)
            deleted_device_links = db_session.query(UserDeviceLink).filter(UserDeviceLink.device_id.in_(dead_device_ids)).delete(synchronize_session=False)

            db_session.commit()

            if len(dead_rasps) != 0:
                await history.log_warning(
                    db=db_session,
                    action="Health check",
                    details=f"Rasps: [{', '.join(dead_rasp_ids)}] went offline",
                )
                for id in dead_rasp_ids:
                    await websocket_handler.toggle_rasp_status(id, "offline")

            if len(dead_devices) != 0:
                await history.log_warning(
                    db=db_session,
                    action="Health check",
                    details=f"Devices: [{', '.join(dead_device_ids)}] went offline",
                )
                for id in dead_device_ids:
                    await websocket_handler.toggle_device_status(id, "offline")
        
        except Exception as e:
            print(f"檢查狀態時出錯: {e}")
        finally:
            db_session.close() 