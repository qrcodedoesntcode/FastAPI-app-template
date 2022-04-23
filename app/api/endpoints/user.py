from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.auth import check_email_is_taken, check_username_is_taken
from app.crud.user import create_new_user
from app.resources import strings
from app.schemas.user import UserCreate, UserSchema

router = APIRouter(prefix="/user")


@router.post("/", name="Create a user", response_model=UserSchema)
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
