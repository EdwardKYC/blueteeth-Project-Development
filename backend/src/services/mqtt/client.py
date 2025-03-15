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
            print("成功連接到 MQTT broker")
        except Exception as e:
            print(f"初始連接失敗，原因: {e}")
            self.connected = False

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for successful connection."""
        if rc == 0:
            print("MQTT 連接成功")
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
                print("嘗試重新連接到 MQTT broker...")
                self.client.reconnect()
                self.client.loop_start() 
                print("重新連接成功")
                self.connected = True
            except Exception as e:
                print(f"重新連接失敗，原因: {e}")
                time.sleep(5)

    def publish(self, topic: str, payload: dict):
        try:
            print(f"發布到主題：{topic}, 資訊如下：{json.dumps(payload)}")
            self.client.publish(topic, json.dumps(payload))
        except Exception as e:
            print(f"發布失敗，原因 {e}")
            self.reconnect()
            self.client.publish(topic, json.dumps(payload))

    def subscribe(self, topic: str, callback):
        """訂閱 MQTT 主題"""
        self.client.subscribe(topic)
        self.client.message_callback_add(topic, callback)