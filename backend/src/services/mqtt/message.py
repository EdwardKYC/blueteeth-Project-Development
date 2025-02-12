from .client import MQTTClient
from src.websockets.manager import SingletonMeta
from sqlalchemy.orm import Session
from src.rasp.models import Device

class MQTTMessageHandler(metaclass=SingletonMeta):
    """Handles application-specific MQTT messages."""
    BROKER_ADDRESS = "mqtt_broker"
    BROKER_PORT = 1883
    TOPIC_TEMPLATE = "rasp/{rasp_id}"

    def __init__(self):
        self.mqtt_client = MQTTClient(broker_address=self.BROKER_ADDRESS, port=self.BROKER_PORT)

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

    