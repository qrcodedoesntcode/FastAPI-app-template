from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import Config
from app.models.user import User


def crud_create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


def check_username_is_taken(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def check_email_is_taken(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
