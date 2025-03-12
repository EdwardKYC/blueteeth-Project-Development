from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.rasp.constants import RelativeDirection
from src.users.models import User, UserDeviceLink, UserRaspLink, UserBookLink
from src.books.models import Book
from src.rasp.models import Rasp, Device
from src.books.exceptions import ResourceAlreadyExistsException, ResourceNotFoundException, ResourceAlreadyDeletedException
from src.services.mqtt.message import MQTTMessageHandler

mqtt_message_handler = MQTTMessageHandler()

def toggle_user_rasp(user: User, db: Session, rasp_id: str = None, color: str = None, direction: RelativeDirection = None):
    if not rasp_id:
        rasp_links = db.query(UserRaspLink).filter(UserRaspLink.user_id == user.id).all()
        if not rasp_links:
            return
        
        for link in rasp_links:
            mqtt_message_handler.cancel_rasp_navigation(rasp_id=link.rasp_id, user_name=user.username)
            db.delete(link)
            
        return

    rasp = db.query(Rasp).filter(Rasp.id == rasp_id).first()
    if not rasp:
        raise ResourceNotFoundException("Rasp", rasp_id)
    
    link = db.query(UserRaspLink).filter(UserRaspLink.user_id == user.id, UserRaspLink.rasp_id == rasp_id).first()
    if link:
        raise ResourceAlreadyExistsException("UserRaspLink", rasp_id)

    if not direction:
        raise ValueError("Direction must be provided to create a new link")

    new_link = UserRaspLink(user_id=user.id, rasp_id=rasp_id, direction=direction.value)
    db.add(new_link)
    mqtt_message_handler.add_rasp_direction(rasp_id=rasp_id, user_name=user.username, direction=direction.value, color=color)


def toggle_user_device(user: User, db: Session, device_id: str = None, color: str = None):
    if not device_id:
        device_link = db.query(UserDeviceLink).filter(UserDeviceLink.user_id == user.id).first()
        if not device_link:
            raise ResourceAlreadyDeletedException()
        else:
            mqtt_message_handler.cancel_device_navigation(device_id=device_link.device_id, user_name=user.username, db=db)
            db.delete(device_link)
        return

    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise ResourceNotFoundException("Device", device_id)

    link = db.query(UserDeviceLink).filter(UserDeviceLink.user_id == user.id, UserDeviceLink.device_id == device_id).first()
    if link:
        raise ResourceAlreadyExistsException("UserDeviceLink", device_id)

    if not color:
         raise ValueError("Color must be provided to create a new link")

    new_link = UserDeviceLink(user_id=user.id, device_id=device_id, color=color)
    db.add(new_link)
    mqtt_message_handler.add_device_color(device_id=device_id, user_name=user.username, color=color, db=db)

def toggle_user_book(user: User, db: Session, book_id: str = None):
    if not book_id:
        book_link = db.query(UserBookLink).filter(UserBookLink.user_id == user.id).first()
        if book_link:
            db.delete(book_link)
        else:
            raise ResourceAlreadyDeletedException()

        return

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise ResourceNotFoundException("Device", book_id)

    link = db.query(UserBookLink).filter(UserBookLink.user_id == user.id, UserBookLink.book_id == book_id).first()
    if link:
        raise ResourceAlreadyExistsException("UserBookLink", book_id)

    new_link = UserBookLink(user_id=user.id, book_id=book_id)
    db.add(new_link)