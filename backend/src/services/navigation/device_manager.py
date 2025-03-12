from src.rasp.models import Device
from src.books.models import Book
from src.users.models import UserDeviceLink

from sqlalchemy import exists
from sqlalchemy.orm import Session
from typing import Tuple
import random
from colorsys import rgb_to_hsv

class DeviceManager:
    def __init__(self, db: Session):
        self.db = db
        self.used_colors = set()

    def get_book_by_id(self, book_id: int) -> Book:
        """根據 ID 查詢書籍"""
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError(f"Book with id {book_id} not found")
        
        if book.device_id:
            device = self.db.query(Device).filter(Device.id == book.device_id).first()
            if not device:
                raise ValueError(f"Book {book_id} is associated with Device {book.device_id}, but the device is missing")
        return book

    def assign_device_color(self, book: Book) -> Tuple[Device, str]:
        """為書本對應的設備分配燈色"""
        if not book.device_id:
            raise ValueError(f"Book {book.id} is not associated with any device")

        device = self.db.query(Device).filter(Device.id == book.device_id).first()
        if not device:
            raise ValueError(f"Device {book.device_id} not found for Book {book.id}")

        unique_color = self.generate_unique_color()
        return device, unique_color

    def generate_unique_color(self) -> str:
        def is_color_too_light(color: str) -> bool:
            hex_color = color.lstrip("#")
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            return brightness >= 180 
        
        def color_distance(color1: str, color2: str) -> float:
            """計算顏色之間的距離（使用 HSV 色彩空間）"""
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            # 轉換為 HSV（避免亮度影響）
            h1, s1, v1 = rgb_to_hsv(r1 / 255.0, g1 / 255.0, b1 / 255.0)
            h2, s2, v2 = rgb_to_hsv(r2 / 255.0, g2 / 255.0, b2 / 255.0)

            # 計算 HSV 距離
            return ((h1 - h2) ** 2 + (s1 - s2) ** 2 + (v1 - v2) ** 2) ** 0.5

        def is_color_too_similar(new_color: str, existing_colors: list[str]) -> bool:
            """檢查新顏色是否與現有顏色過於相似"""
            return any(color_distance(new_color, existing) < 0.2 for existing in existing_colors)

        existing_colors = [
            row[0] for row in self.db.query(UserDeviceLink.color).all()
        ]

        while True:
            color = f"#{random.randint(0, 0xFFFFFF):06x}"

            if not is_color_too_light(color) and not is_color_too_similar(color, existing_colors):
                return color