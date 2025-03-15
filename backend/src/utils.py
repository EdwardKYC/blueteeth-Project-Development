from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import asyncio
from src.dependencies import get_db
from src.rasp.models import Rasp, Device
from src.history.service import HistoryService
from src.websockets import WebSocketMessageHandler

history = HistoryService()
websocket_handler = WebSocketMessageHandler()

async def check_alive_status(db: Session = Depends(get_db)):
    while True:
        await asyncio.sleep(30)  
        # print("檢查裝態")
        db_session = next(get_db())

        try:
            now = datetime.utcnow()
            one_minute_ago = now - timedelta(seconds=30)

            dead_rasps = db_session.query(Rasp).filter(Rasp.last_update < one_minute_ago, Rasp.status == "online").all()
            dead_devices = db_session.query(Device).filter(Device.last_update < one_minute_ago, Device.status == "online").all()

            for rasp in dead_rasps:
                rasp.status = "offline"
            for device in dead_devices:
                device.status = "offline"

            db_session.commit()
            dead_rasp_ids = [rasp.id for rasp in dead_rasps]
            dead_device_ids = [device.id for device in dead_devices]

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

_main_loop = None

def set_main_loop(loop: asyncio.AbstractEventLoop):
    global _main_loop
    _main_loop = loop

def get_main_loop() -> asyncio.AbstractEventLoop:
    return _main_loop