from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash
from app.modules.users.models import User
from app.modules.users.schema import UserCreate
from app.services import strings


async def check_username_is_taken(db: AsyncSession, username: str) -> bool:
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN,
        )
    return False


async def check_email_is_taken(db: AsyncSession, email: str) -> bool:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)

    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )
    return False


async def create_new_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
        is_active=user.is_active,
    )
    db.add(db_user)
    await db.commit()
    return db_user
