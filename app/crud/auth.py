from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate


async def check_username_is_taken(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()


async def check_email_is_taken(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()


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
