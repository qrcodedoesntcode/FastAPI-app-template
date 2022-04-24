from typing import Union

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.resources import strings

IdType = Union["int", "str"]


def get_user_by_user_id(db: Session, user_id: IdType):
    if isinstance(user_id, int):
        return db.query(User).filter(User.id == user_id).first()

    return db.query(User).filter(User.username == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session, page: int = 1, per_page: int = 100):
    return db.query(User).limit(per_page).offset((page - 1) * per_page).all()


def delete_user_by_user_id(db, user_id: IdType):
    db_user = get_user_by_user_id(db, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )

    db.delete(db_user)
    db.commit()

    return {"success": True}
