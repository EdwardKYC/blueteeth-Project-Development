from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import SQLAlchemyError
from jose import jwt, JWTError

from sqlalchemy.orm import Session

from src.config import global_config
from .models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=global_config.AUTH_TOKEN_URL)

def verify_password(current_password, correct_password):
    return current_password == correct_password


def validate_user_credentials(db_session: Session, username: str, password: str):
    try:
        user = db_session.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=401, detail="Invalid username or password."
            )
        return user
    except SQLAlchemyError as db_exc:
        raise HTTPException(
            status_code=500, detail="Database error occurred while validating user credentials."
        ) from db_exc
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred during user validation."
        ) from e


def create_access_token(user_data, expires_delta=None):
    to_encode = user_data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=global_config.DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, global_config.SECRET_KEY, algorithm=global_config.ALGORITHM)
    except JWTError as jwt_exc:
        raise HTTPException(
            status_code=500, detail="Failed to create access token due to encoding error."
        ) from jwt_exc
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred while creating access token."
        ) from e
    
    return encoded_jwt