from src.rasp.models import Device
from src.books.models import Book
from src.users.models import UserDeviceLink

from sqlalchemy import exists
from sqlalchemy.orm import Session
from typing import Tuple
import random

class DeviceManager:
    def __init__(self, db: Session):
        self.db = db
        self.used_colors = set()

    def get_book_by_id(self, book_id: int) -> Book:
        """根據 ID 查詢書籍"""
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError(f"Book with id {book_id} not found")
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
            return brightness > 220 

        while True:
            color = f"#{random.randint(0, 0xFFFFFF):06x}"
            exists_color = self.db.query(
                exists().where(UserDeviceLink.color == color)
            ).scalar()
            if not exists_color and not is_color_too_light(color):
                return color