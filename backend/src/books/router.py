from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from src.dependencies import get_db, get_current_user
from src.books.service import search_books
from src.books.models import Book
from src.users.models import User
from src.rasp.models import Device, Rasp
from src.rasp.service import toggle_user_device, toggle_user_rasp, toggle_user_book
from src.services.navigation.navigator import Navigator
from src.websockets import WebSocketMessageHandler
from src.history.service import HistoryService
from src.books.exceptions import ResourceAlreadyExistsException, ResourceNotFoundException, ResourceAlreadyDeletedException, NoAvailableColorException
from .schemas import SearchBookSchema, RegisterBookSchema, NavigateBookSchema
from src.books.models import BookBorrowHistory

from datetime import datetime
import pytz
from typing import List

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    responses={404: {"description": "Not found"}},
)

history = HistoryService()
websocket_message_handler = WebSocketMessageHandler()

@router.post("/search_book", response_model=List[dict])
async def search_book_endpoint(
    params: SearchBookSchema, 
    user=Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    search_term = params.search_term
    books = search_books(db, search_term)

    if not books:
        await history.log_info(
            db=db, 
            action="Search Book", 
            details=f"No books found for search term: '{search_term}' by user: {user.username}"
        )
        raise HTTPException(status_code=404, detail="No books found matching the search term.")

    await history.log_info(
        db=db, 
        action="Search Book", 
        details=f"User '{user.username}' found {len(books)} books for search term: '{search_term}'"
    )
    return [{"id": book.id, "name": book.name, "description": book.description} for book in books]

@router.post("/register-book")
async def register_book(
    params: RegisterBookSchema, 
    db: Session = Depends(get_db)
):
    """
    註冊書籍
    """
    name = params.name
    device_id = params.device_id
    description = params.description

    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        await history.log_warning(db=db, action="Register Book", details=f"Device ID '{device_id}' not found while registering book '{name}'")
        raise HTTPException(status_code=404, detail=f"Device with id {device_id} not found")
    
    new_book = Book(name=name, description=description, device_id=device_id)
    db.add(new_book)

    try:
        db.commit()
        db.refresh(new_book)

    except SQLAlchemyError as e:
        db.rollback()
        await history.log_error(db=db, action="Register Book", details=f"Database error while registering book '{name}' on device ID: {device_id}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to register the book due to a database error.")
    
    except Exception as e:
        db.rollback()
        await history.log_error(db=db, action="Register Book", details=f"Unexpected error while registering book '{name}' on device ID: {device_id}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while registering the book.")
    
    await websocket_message_handler.register_book(book=new_book)
    await history.log_info(db=db, action="Register Book", details=f"Book '{name}' successfully registered on device ID: {device_id}")
    return new_book.to_dict()

@router.delete("/delete-book/{book_id}")
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    """
    刪除指定 ID 的書籍。
    """
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        await history.log_warning(
            db=db, action="Delete Book",
            details=f"Delete a non-existent book ID '{book_id}'"
        )
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    try:
        if book.device:
            book.device_id = None

        db.delete(book)
        db.commit()

        await history.log_info(
            db=db, action="Delete Book",
            details=f"Book '{book.name}' (ID: {book_id}) deleted"
        )

        return {"message": f"Book '{book.name}' successfully deleted"}

    except SQLAlchemyError as e:
        db.rollback()
        await history.log_error(
            db=db, action="Delete Book",
            details=f"Database error while deleting book '{book_id}': {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Failed to delete book due to database error.")

    except Exception as e:
        db.rollback()
        await history.log_error(
            db=db, action="Delete Book",
            details=f"Unexpected error while deleting book '{book_id}': {str(e)}"
        )
        raise HTTPException(status_code=500, detail="An unexpected error occurred while deleting the book.")

@router.get("/get-all-books", response_model=List[dict])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return [
        {
            "id": book.id,
            "name": book.name,
            "description": book.description,
            "device_id": book.device_id,
        }
        for book in books
    ]

@router.post("/navigate")
async def navigate_to_book(
    params: NavigateBookSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    導航到指定書籍，更新用戶的 Rasp 和 Device 資料。
    """
    book_id = params.book_id

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        await history.log_warning(db=db, action="Navigate", details=f"{user.username} try to navigate bookId {book_id}, which doesn't exist")
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    navigator = Navigator(db)

    try:
        rasp_directions, device, unique_color = navigator.navigate_to_book(book_id)
    except NoAvailableColorException as e:
        db.rollback()
        await history.log_warning(
            db=db, action="Navigate",
            details=f"Failed to navigate due to color exhaustion for user: {user.username}"
        )
        raise HTTPException(status_code=400, detail="Navigation failed: no available colors left.")
    except ValueError as e:
        await history.log_warning(db=db, action="Navigate", details=f"Can't find a path for book(name: {book.name}, id: {book_id}), user: {user.username}. {str(e)}")
        raise HTTPException(status_code=400, detail=f"Can't find a path for book id {book.id}.")
    except Exception as e:
        await history.log_error(db=db, action="Navigate", details=f"Unexpected error during navigation: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    try:
        for rasp_id, direction in rasp_directions:
            toggle_user_rasp(rasp_id=rasp_id, user=user, db=db, direction=direction, color=unique_color)
            await websocket_message_handler.add_rasp_direction(rasp_id=rasp_id, username=user.username, direction=direction.value, color=unique_color)

        toggle_user_book(book_id=book_id, user=user, db=db)
        await websocket_message_handler.navigate_book(book_id=book_id, book_name=book.name, username=user.username)

        toggle_user_device(device_id=device.id, user=user, db=db, color=unique_color)
        await websocket_message_handler.add_device_color(device_id=device.id, username=user.username, color=unique_color)
        taipei_tz = pytz.timezone("Asia/Taipei")
        borrow_record = BookBorrowHistory(
            user_id=user.id,
            book_id=book.id,
            type="start-nav",
            color=unique_color,
            timestamp=datetime.now(taipei_tz),
        )
        
        db.add(borrow_record)
        db.flush()
        await websocket_message_handler.add_book_history(borrow_record)
        db.commit()

    except ResourceAlreadyExistsException as e:
        db.rollback()
        await history.log_warning(db=db, action="Navigate", details=f"User {user.username} is trying to navigate to book {book.name}, but they are already in a navigating state.")
        raise HTTPException(status_code=400, detail="Failed to navigate, user already navigating.")

    except (ResourceNotFoundException, ValueError) as e:
        db.rollback()
        await history.log_error(db=db, action="Navigate", details=str(e))
        raise HTTPException(status_code=500, detail="Unexcepted error occur. Failed to navigate to the book.")

    except SQLAlchemyError as e:
        db.rollback()
        await history.log_error(db=db, action="Navigate", details=f"Navigation failed for user {user.username}. Database error: {str(e)}.")
        raise HTTPException(status_code=500, detail="Unexcepted error occur. Failed to navigate to the book.")
    
    except Exception as e:
        db.rollback()
        await history.log_error(db=db, action="Navigate", details=f"Unexpected error: {str(e)}.")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while navigating.")
    
    navigation_details = (
        f"Navigation to book {book.name} successful. "
        f"user: {user.username}, "
        f"controled device: {device.id}, "
        f"displayed color: {unique_color}, "
        f"rasps: [{' | '.join(f'id: {id}, direction: {direction.value}' for id, direction in rasp_directions)}]"
    )
    await history.log_info(db=db, action="Navigate", details=navigation_details)

    return {
        "message": f"Successfully navigate for user {user.username}",
        "displayed_color": unique_color,
    }

@router.post("/cancel-navigation")
async def cancel_navigation(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    取消當前用戶的導航，清除所有 Rasp 和 Device 關聯。
    """
    try:
        toggle_user_rasp(user, db)
        toggle_user_device(user, db)
        toggle_user_book(user, db)
        db.commit()

    except ResourceAlreadyDeletedException as e:
        db.rollback()
        await history.log_warning(db=db, action="Cancel Navigation", details=f"User {user.username} is trying to cancel navigation, but it had been canceled already.")
        raise HTTPException(status_code=400, detail="Failed to cancel navigation, it had been canceled already.")

    except SQLAlchemyError as e:
        db.rollback()  
        await history.log_error(db=db, action="Cancel Navigation", details=f"Database error: {str(e)}.")
        raise HTTPException(status_code=500, detail="Failed to cancel navigation due to database error.")

    except Exception as e:
        db.rollback() 
        await history.log_error(db=db, action="Cancel Navigation", details=f"Unexpected error: {str(e)}.")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while canceling navigation.")
    
    await websocket_message_handler.cancel_navigation(user.username)
    await history.log_info(db=db, action="Cancel Navigation", details=f"Successfully canceled navigation for user: {user.username}.")
    return {"message": "Successfully canceled navigation!"}

@router.get("/borrow-history", response_model=List[dict])
async def get_user_borrow_history(
    db: Session = Depends(get_db)
):
    records = db.query(BookBorrowHistory).order_by(BookBorrowHistory.timestamp.desc()).all()
    return [
            {
                "id": r.id,
                "book_id": r.book.id,
                "color": r.color,
                "username": r.user.username,
                "timestamp": r.timestamp.isoformat()
            }
            for r in records
        ]

@router.delete("/delete-borrow-history/{book_id}")
async def delete_borrow_history_by_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    try:
        records = db.query(BookBorrowHistory).filter(BookBorrowHistory.book_id == book_id).all()

        if not records:
            raise HTTPException(status_code=404, detail=f"No borrow history found for book ID {book_id}.")

        for record in records:
            db.delete(record)
        db.commit()

        await history.log_info(
            db=db,
            action="Delete Borrow History",
            details=f"Deleted {len(records)} borrow history records for book ID: {book_id}"
        )

        return {"message": f"Successfully deleted {len(records)} borrow records for book ID {book_id}"}

    except SQLAlchemyError as e:
        db.rollback()
        await history.log_error(
            db=db,
            action="Delete Borrow History",
            details=f"Database error: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Database error occurred while deleting borrow history.")