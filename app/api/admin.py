from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.user import (
    get_all_users,
)
from app.models.database import get_db
from app.schemas.user import User

router = APIRouter(prefix="/admin")


@router.get("/user", response_model=List[User], name="Get all users")
def get_users(
    page: int = 1,
    per_page: int = 100,
    db: Session = Depends(get_db),
):
    users = get_all_users(db, page=page, per_page=per_page)

    return users
