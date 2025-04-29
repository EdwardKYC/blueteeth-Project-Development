from .device_manager import DeviceManager
from src.services.navigation.map_builder import MapGraph

from sqlalchemy.orm import Session

class Navigator:
    def __init__(self, db: Session):
        self.db = db

    def navigate_to_book(self, book_id):
        """導航至指定書籍位置"""
        map = MapGraph(self.db)
        device_manager = DeviceManager(self.db)

        # 查詢書籍
        book = device_manager.get_book_by_id(book_id)
        directions = map.find_path(book.cord_x, book.cord_y)

        if len(directions) == 0:
            raise ValueError("No path found to the target Rasp")
        
        device, unique_color = device_manager.assign_device_color(book)

        return directions, device, unique_color