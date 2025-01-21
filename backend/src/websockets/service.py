from .manager import WebSocketManager, SingletonMeta
from src.history.models import HistoryLog
from src.rasp.models import Rasp, Device
from src.books.models import Book
from src.users.models import User

class WebSocketMessageHandler(metaclass=SingletonMeta):
    def __init__(self):
        self.manager = WebSocketManager()

    async def add_device_color(self, username: str, device_id: str, color: str):
        """發送 add_device_color 消息"""
        message = {
            "type": "add_device_color",
            "payload": {
                "username" : username,
                "device_id": device_id,
                "color": color
            }
        }
        await self.manager.send_message(message)

    async def cancel_navigation(self, username: str):
        """發送 cancel_navigation 消息"""
        message = {
            "type": "cancel_navigation",
            "payload": {
                "username" : username
            }
        }
        await self.manager.send_message(message)

    async def add_rasp_direction(self, rasp_id: str, username: str, direction: str):
        """發送 add_rasp_direction 消息"""
        message = {
            "type": "add_rasp_direction",
            "payload": {"rasp_id": rasp_id, "username": username, "direction": direction}
        }
        await self.manager.send_message(message)

    async def navigate_book(self, book_id: int, book_name: str, username: str):
        """發送 navigate_book 消息"""
        message = {
            "type": "navigate_book",
            "payload": {"book_id": book_id, "book_name": book_name, "username": username}
        }
        await self.manager.send_message(message)

    async def update_device_battery(self, device_id: str, battery: int):
        message = {
            "type": "update_device_battery",
            "payload": {"device_id": device_id, "battery": battery}
        }
        await self.manager.send_message(message)

    async def add_history_log(self, history: HistoryLog):
        """發送 navigate_book 消息"""
        message = {
            "type": "add_history_log",
            "payload": {
                "id" : history.id,
                "type" : history.type,
                "action" : history.action,
                "timestamp": history.timestamp.isoformat(),
                "details" : history.details
            }
        }
        await self.manager.send_message(message)

    async def clear_all_history(self):
        message = {
            "type": "clear_all_history"
        }
        await self.manager.send_message(message)

    async def register_book(self, book: Book):
        message = {
            "type": "register_book",
            "payload" : {
                "id": book.id,
                "name": book.name,
                "description": book.description,
                "device_id": book.device_id,
            }
        }
        await self.manager.send_message(message)

    async def register_rasp(self, rasp: Rasp):
        message = {
            "type": "register_rasp",
            "payload" : {
                "id": rasp.id,
                "cords": {"x": rasp.cord_x, "y": rasp.cord_y},
                "facing": rasp.facing
            }
        }
        await self.manager.send_message(message)

    async def register_device(self, device: Device):
        message = {
            "type": "register_device",
            "payload" : {
                "id": device.id,
                "battery": device.battery,
                "cords": {"x": device.cord_x, "y": device.cord_y},
                "rasp_id": device.rasp.id if device.rasp else None
            }
        }
        await self.manager.send_message(message)

    async def register_user(self, user: User):
        message = {
            "type": "register_user",
            "payload" : {
                "username": user.username,
                "rasps": [
                    {
                        "id": link.rasp.id,
                        "direction": link.direction
                    }
                    for link in user.current_rasps
                ],
                "device": {
                    "id": user.current_device.device.id,
                    "color": user.current_device.color
                } if user.current_device else None,
                "book": {
                    "id": user.current_book.book.id,
                    "name": user.current_book.book.name,
                } if user.current_book else None
            }
        }
        await self.manager.send_message(message)