import time
import paho.mqtt.client as mqtt
import json
from src.websockets.manager import SingletonMeta

class MQTTClient(metaclass=SingletonMeta):
    """Basic MQTT Client wrapper for connecting, publishing, and handling events."""
    def __init__(self, broker_address: str, port: int):
        self.broker_address = broker_address
        self.port = port
        self.client = mqtt.Client()
        self.connected = False

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

        self._connect()
        
    def _connect(self):
        try:
            self.client.connect(self.broker_address, self.port)
            self.client.loop_start()  
        except Exception as e:
            print(f"初始連接失敗，原因: {e}")
            self.connected = False

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for successful connection."""
        if rc == 0:
            self.connected = True
        else:
            print(f"MQTT 連接失敗，返回代碼: {rc}")
            self.connected = False

    def _on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects."""
        print("MQTT 連接斷開")
        self.connected = False
        
    def reconnect(self):
        """Reconnect to the MQTT broker."""
        while not self.connected:
            try:
                self.client.reconnect()
                self.client.loop_start() 
                self.connected = True
            except Exception as e:
                print(f"重新連接失敗，原因: {e}")
                time.sleep(5)

    def publish(self, topic: str, payload: dict):
        try:
            self.client.publish(topic, json.dumps(payload))
        except Exception as e:
            print(f"發布失敗，原因 {e}")
            self.reconnect()
            self.client.publish(topic, json.dumps(payload))