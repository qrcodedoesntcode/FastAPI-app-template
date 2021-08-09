from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import Config
from app.crud.user import crud_create_user, crud_get_user, crud_get_users
from app.models.database import get_db
from app.schemas import user

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = crud_get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user


@router.post("/")
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    return crud_create_user(db=db, user=user)


@router.get("/", response_model=List[user.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    users = crud_get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user
