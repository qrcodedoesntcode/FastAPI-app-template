from typing import Union

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.resources import strings

IdType = Union["int", "str"]


async def get_user_by_user_id(db: Session, user_id: IdType):
    if isinstance(user_id, int):
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    stmt = select(User).where(User.username == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_user_by_username(db: Session, username: str):
    stmt = select(User).filter(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_all_users(db: Session, page: int = 1, per_page: int = 100):
    stmt = select(User).offset(per_page * (page - 1)).limit(per_page)
    result = await db.execute(stmt)
    return result.scalars().all()


async def delete_user_by_user_id(db, user_id: IdType):
    db_user = await get_user_by_user_id(db, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )

    await db.delete(db_user)
    await db.commit()

    return {"success": True}
