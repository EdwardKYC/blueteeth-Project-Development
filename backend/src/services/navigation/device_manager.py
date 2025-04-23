from src.rasp.models import Device
from src.books.models import Book
from src.users.models import UserDeviceLink
from src.books.exceptions import NoAvailableColorException

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
            if not device or device.status == "offline":
                raise ValueError(f"Book {book_id} is associated with Device {book.device_id}, but the device is either missing or offline")
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
        available_colors = [
            "#ff0000",  # Red
            "#00ff00",  # Green
            "#0000ff",  # Blue
            "#ffff00",  # Yellow
            "#ff00ff",  # crimson
            "#00ffff",  # Aqua
            "#ffa500",  # Orange
        ]

        used_colors = {row[0] for row in self.db.query(UserDeviceLink.color).all() if row[0]}

        unused_colors = [color for color in available_colors if color not in used_colors]

        if not unused_colors:
            raise NoAvailableColorException()

        return random.choice(unused_colors)