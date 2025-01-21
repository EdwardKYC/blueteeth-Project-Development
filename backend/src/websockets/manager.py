from typing import Dict
from fastapi import WebSocket

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class WebSocketManager(metaclass=SingletonMeta):
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        """新增一個 WebSocket 連接"""
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        """移除一個 WebSocket 連接"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_message(self, message: dict):
        """向特定客戶端發送消息"""
        disconnected_clients = []
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Failed to send message to {client_id}: {e}")
                disconnected_clients.append(client_id)

        for client_id in disconnected_clients:
            self.disconnect(client_id)

    async def broadcast(self, message: dict):
        """向所有客戶端廣播消息"""
        for websocket in self.active_connections.values():
            await websocket.send_json(message)