from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    current_rasps = relationship("UserRaspLink", back_populates="user")
    current_book = relationship("UserBookLink", back_populates="user", uselist=False)
    current_device = relationship("UserDeviceLink", back_populates="user", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "rasps": [
                {
                    "id": link.rasp.id,
                    "direction": link.direction
                }
                for link in self.current_rasps
            ],
            "device": {
                "id": self.current_device.device.id,
                "color": self.current_device.color
            } if self.current_device else None
        }
    

class UserBookLink(Base):
    __tablename__ = "user_book_link"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)

    user = relationship("User", back_populates="current_book")
    book = relationship("Book")

class UserDeviceLink(Base):
    __tablename__ = "user_device_link"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    device_id = Column(String, ForeignKey("devices.id"), primary_key=True)
    color = Column(String, nullable=False)

    user = relationship("User", back_populates="current_device")
    device = relationship("Device")
    
class UserRaspLink(Base):
    __tablename__ = "user_rasp_link"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    rasp_id = Column(String, ForeignKey("rasps.id"), primary_key=True)
    direction = Column(String, nullable=False) 

    user = relationship("User", back_populates="current_rasps")
    rasp = relationship("Rasp")