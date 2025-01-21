from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    device_id = Column(String, ForeignKey("devices.id"), nullable=True)
    device = relationship("Device", back_populates="books")
    
    @property
    def cord_x(self):
        return self.device.cord_x if self.device else None

    @property
    def cord_y(self):
        return self.device.cord_y if self.device else None
      
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "device_id": self.device_id,
            "location": {"x": self.cord_x, "y": self.cord_y},
        }