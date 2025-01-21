from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Rasp(Base):
    __tablename__ = "rasps"

    id = Column(String, primary_key=True, index=True)
    cord_x = Column(Integer, nullable=False)
    cord_y = Column(Integer, nullable=False)
    facing = Column(String, nullable=False)

    devices = relationship("Device", back_populates="rasp")
    
    def to_dict(self):
            return {
                "id": self.id,
                "location": {"x": self.cord_x, "y": self.cord_y},
                "facing": self.facing,
                "devices": [{
                     "id" : device.id,
                     "location": {"x": device.cord_x, "y": device.cord_y}
                } for device in self.devices],
            }
    
class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, index=True)
    battery = Column(Integer, nullable=False)
    cord_x = Column(Integer, nullable=False)
    cord_y = Column(Integer, nullable=False)
    
    rasp_id = Column(String, ForeignKey("rasps.id"), nullable=True)
    rasp = relationship("Rasp", back_populates="devices")
    books = relationship("Book", back_populates="device")
    
    def to_dict(self):
        return {
            "id": self.id,
            "battery": self.battery,
            "location": {"x": self.cord_x, "y": self.cord_y},
          	"books": [book.to_dict() for book in self.books],
            "rasp": {
                "id": self.rasp.id,
                "location": {"x": self.rasp.cord_x, "y": self.rasp.cord_y},
                "facing": self.rasp.facing,
            } if self.rasp else None,
        }