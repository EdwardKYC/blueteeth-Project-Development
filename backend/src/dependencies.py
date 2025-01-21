from fastapi import Depends
from jose import jwt, JWTError
from fastapi import HTTPException

from src.database import engine, SessionLocal
from src.config import global_config
from .users.models import User
from .users.service import oauth2_scheme

def get_db():
    session = SessionLocal(bind=engine)
    try:
        yield session
    finally:
        session.close()

def get_current_user(
    token = Depends(oauth2_scheme),
    db = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, global_config.SECRET_KEY, algorithms=global_config.ALGORITHM)
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="Invalid token: missing username")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user