from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.api.deps import get_db
from app.crud.admin import delete_user_by_user_id, get_all_users, get_user_by_user_id
from app.resources import strings
from app.schemas.user import UserSchema

router = APIRouter(prefix="/admin")
IdType = Union[int, str]


@router.get("/users", response_model=List[UserSchema], name="Get all users")
async def get_users(
    page: int = 1,
    per_page: int = 100,
    db: Session = Depends(get_db),
):
    users = await get_all_users(db, page=page, per_page=per_page)

    return users


@router.get(
    "/users/{user_id}",
    response_model=UserSchema,
    name="Get specific user by user_id (id or email)",
)
async def get_specific_user(user_id: IdType, db: Session = Depends(deps.get_db)):
    db_user = await get_user_by_user_id(db, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
    return db_user


@router.delete(
    "/users/{user_id}",
    name="Delete specific user by user_id (id or email)",
)
async def delete_specific_user(user_id: IdType, db: Session = Depends(deps.get_db)):
    return await delete_user_by_user_id(db, user_id)
