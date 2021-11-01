from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import Config
from app.crud.auth import check_email_is_taken, check_username_is_taken
from app.crud.user import create_new_user, get_user_by_id, get_user_by_username
from app.models.database import get_db
from app.resources import strings
from app.schemas.user import User, UserCreate

router = APIRouter(prefix="/user")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{Config.API_V1_STR}/login")


@router.get("/current", response_model=User, name="Get current user")
def get_current_user(
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
    user = get_user_by_username(db, username=token_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
    return user


@router.post("/", name="Create a user", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if check_username_is_taken(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN,
        )

    if check_email_is_taken(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )
    return create_new_user(db=db, user=user)


@router.get("/{user_id}", response_model=User, name="Get specific user by id")
def get_specific_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
    return db_user
