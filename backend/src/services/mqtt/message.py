from .client import MQTTClient
from src.websockets.manager import SingletonMeta
from src.dependencies import get_db
import json
import asyncio
from datetime import datetime
from src.rasp.models import Rasp
from sqlalchemy.orm import Session
from src.rasp.models import Device
from src.websockets import WebSocketMessageHandler
from src.utils import get_main_loop

websocket_handler = WebSocketMessageHandler()

class MQTTMessageHandler(metaclass=SingletonMeta):
    """Handles application-specific MQTT messages."""
    BROKER_ADDRESS = "mqtt_broker"
    BROKER_PORT = 1883
    TOPIC_TEMPLATE = "rasp/{rasp_id}"
    RASP_HEARTBEAT_TOPIC = "rasp/heartbeat"

    def __init__(self):
        self.mqtt_client = MQTTClient(broker_address=self.BROKER_ADDRESS, port=self.BROKER_PORT)
        self.mqtt_client.subscribe(self.RASP_HEARTBEAT_TOPIC, self._on_heartbeat_message)

    def _on_heartbeat_message(self, client, userdata, msg):
        """處理 Raspberry Pi 發送的 heartbeat 訊息"""
        db: Session = next(get_db())
        try:
            payload = json.loads(msg.payload)
            rasp_id = payload.get("rasp_id")

            if not rasp_id:
                print("收到無效的 heartbeat 訊息")
                return

            rasp = db.query(Rasp).filter(Rasp.id == rasp_id).first()
            if rasp:
                rasp.last_update = datetime.utcnow()
                if rasp.status == "offline":
                    rasp.status = "online"
                    main_loop = get_main_loop()
                    if main_loop:
                        # 使用 run_coroutine_threadsafe 提交 coroutine 到主事件迴圈
                        asyncio.run_coroutine_threadsafe(
                            websocket_handler.toggle_rasp_status(rasp.id, "online"),
                            main_loop
                        )
                    else:
                        print("找不到主事件迴圈，無法發送 WebSocket 更新")

                db.commit()
                print(f"更新 Rasp {rasp_id} 為 online，last_update 設為現在時間")

        except Exception as e:
            print(f"處理 MQTT Heartbeat 訊息時出錯: {e}")
        finally:
            db.close()  # 確保關閉 session，避免連線洩漏

    def _get_rasp_id_from_device(self, device_id: str, db: Session) -> str:
        """Fetch the associated rasp_id for a given device_id."""
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device or not device.rasp_id:
            raise ValueError(f"No associated rasp found for device_id {device_id}")
        return device.rasp_id

    def add_rasp_direction(self, rasp_id: str, user_name: str, direction: str, color: str):
        topic = self.TOPIC_TEMPLATE.format(rasp_id=rasp_id)
        payload = {
            "action": "add_rasp_direction",
            "userName": user_name,
            "direction": direction,
            "color": color
        }
        self.mqtt_client.publish(topic, payload)

    def add_device_color(self, user_name: str, device_id: str, color: str, db: Session):
        """Publish device color update message."""
        rasp_id = self._get_rasp_id_from_device(device_id, db)
        topic = self.TOPIC_TEMPLATE.format(rasp_id=rasp_id)
        payload = {
            "action": "add_device_color",
            "userName": user_name,
            "color": color,
            "deviceId": device_id
        }
        self.mqtt_client.publish(topic, payload)

    def cancel_device_navigation(self, device_id: str, user_name: str, db: Session):
        """Publish navigation cancellation message."""
        rasp_id = self._get_rasp_id_from_device(device_id, db)
        topic = self.TOPIC_TEMPLATE.format(rasp_id=rasp_id)
        payload = {
            "action": "cancel_device_navigation",
            "userName": user_name,
            "deviceId": device_id
        }
        self.mqtt_client.publish(topic, payload)

    def cancel_rasp_navigation(self, rasp_id: str, user_name: str):
        """Publish navigation cancellation message."""
        topic = self.TOPIC_TEMPLATE.format(rasp_id=rasp_id)
        payload = {
            "action": "cancel_rasp_navigation",
            "userName": user_name
        }
        self.mqtt_client.publish(topic, payload)

    def start(self):
        """啟動 MQTT 訂閱"""
        self.mqtt_client.client.loop_start()