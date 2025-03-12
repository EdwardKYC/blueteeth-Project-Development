from .node import Node
from .device_manager import DeviceManager
from .direction_calculator import DirectionCalculator
from src.services.maps.map_builder import MapGraph

from sqlalchemy.orm import Session

class Navigator:
    def __init__(self, db: Session):
        self.db = db

    def navigate_to_book(self, book_id):
        """導航至指定書籍位置"""
        map = MapGraph(self.db)
        device_manager = DeviceManager(self.db)
        direction_calculator = DirectionCalculator()

        # 查詢書籍
        book = device_manager.get_book_by_id(book_id)
        print(f"書本: {book.cord_x, book.cord_y}")

        # 找到起始位置和最近的 Rasp
        start_node = map.find_closest_node(0, 0)
        closest_rasp_to_book = map.find_closest_node(book.cord_x, book.cord_y)

        if not closest_rasp_to_book:
            raise ValueError("No Rasp found near the book")

        # 計算最短路徑
        path = map.find_shortest_path(start_node, closest_rasp_to_book)
        if not path:
            raise ValueError("No path found to the target Rasp")

        # 加入書籍位置作為虛擬終點
        book_virtual_node = Node("VirtualBook", book.cord_x, book.cord_y, None)
        path.append(book_virtual_node)

        # 分配導航指令
        directions = direction_calculator.assign_directions(path)
        device, unique_color = device_manager.assign_device_color(book)

        return directions, device, unique_color