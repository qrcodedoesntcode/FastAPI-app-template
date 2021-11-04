from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from app import models
from app.core.config import settings
from app.crud.user import get_user_by_username, is_active
from app.models.database import SessionLocal
from app.resources import strings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except jwt.JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )

    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
):
    if not is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INACTIVE_USER
        )
    return current_user
