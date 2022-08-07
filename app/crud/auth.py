from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate


async def check_username_is_taken(db: Session, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()


async def check_email_is_taken(db: Session, email: str):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_new_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
        is_active=user.is_active,
    )
    db.add(db_user)
    await db.commit()
    return db_user
