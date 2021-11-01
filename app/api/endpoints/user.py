from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.api import deps
from app.crud.auth import check_email_is_taken, check_username_is_taken
from app.crud.user import create_new_user, get_user_by_id
from app.resources import strings
from app.schemas.user import User, UserCreate

router = APIRouter(prefix="/user")


@router.get("/", response_model=User, name="Get current user")
def get_current_user(current_user: models.User = Depends(deps.get_current_user)):
    return current_user


@router.post("/", name="Create a user", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(deps.get_db)):
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
def get_specific_user(user_id: int, db: Session = Depends(deps.get_db)):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
    return db_user
