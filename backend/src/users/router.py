from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies import get_db, get_current_user
from src.users.schemas import UserAuthSchema
from src.users.models import User
from src.users.config import user_config
from src.history.service import HistoryService
from src.websockets.service import WebSocketMessageHandler
from src.users.service import (
    validate_user_credentials,
    create_access_token,
)


history = HistoryService()
websocket_message_handler = WebSocketMessageHandler()

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Authenticates a user and generates an access token.

    :param form_data: Form data containing username and password.
    :param db: Database session dependency.
    :return: JSON with access token and token type.
    """
    try:
        user = validate_user_credentials(db, form_data.username, form_data.password)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        access_token = create_access_token(
            user_data={"sub": str(user.username)}, 
            expires_delta=timedelta(minutes=user_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        await history.log_info(db=db, action="Login", details=f"User {user.username} has logged in.")
        return {
            "message": "Logged in successfully.",
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    except HTTPException as http_exc:
        await history.log_info(db=db, action="Login", details=f"User {form_data.username} failed to login. {http_exc.detail}")
        raise http_exc
    
    except Exception as e:
        await history.log_error(db=db, action="Login", details=f"Unexpected error during login. error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@router.post("/register")
async def create_user(user: UserAuthSchema, db: Session = Depends(get_db)):
    """
    Registers a new user with a hashed password.

    :param user: User data containing username and password.
    :param db: Database session dependency.
    :return: The created user object.
    """
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username is already taken. Please choose another."
        )
    hashed_password = user.password
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)

    except Exception as e:
        await history.log_error(db=db, action="Create user", details=f"Unexpected error happened during creating user. error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during registration. Please try again.",
        ) from e

    await history.log_info(db=db, action="Create user", details=f"User has been created. user: {db_user.username}")
    await websocket_message_handler.register_user(db_user)
    return {
        "message": "User registered successfully.",
        "username": db_user.username
    }

@router.get("/me")
def read_users_me(user: User = Depends(get_current_user)):
    return user.to_dict()

@router.get("/get-all-users", response_model=list)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "username": user.username,
            "rasps": [
                {
                    "id": link.rasp.id,
                    "direction": link.direction
                }
                for link in user.current_rasps
            ],
            "device": {
                "id": user.current_device.device.id,
                "color": user.current_device.color
            } if user.current_device else None,
            "book": {
                "id": user.current_book.book.id,
                "name": user.current_book.book.name,
            } if user.current_book else None
        }
        for user in users
    ]
