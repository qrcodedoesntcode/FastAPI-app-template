from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.api.deps import get_db
from app.crud.admin import get_all_users, get_user_by_email, get_user_by_id
from app.resources import strings
from app.schemas.user import UserSchema

router = APIRouter(prefix="/admin")


@router.get("/user", response_model=List[UserSchema], name="Get all users")
def get_users(
    page: int = 1,
    per_page: int = 100,
    db: Session = Depends(get_db),
):
    users = get_all_users(db, page=page, per_page=per_page)

    return users


@router.get(
    "/{user_id}",
    response_model=UserSchema,
    name="Get specific user by id or email",
    description='Get specific user by "user_id" where "user_id" is id or email',
)
def get_specific_user(user_id: Union[int, str], db: Session = Depends(deps.get_db)):
    if isinstance(user_id, int):
        db_user = get_user_by_id(db, user_id=user_id)
    else:
        db_user = get_user_by_email(db, email=user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
    return db_user
