from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.modules.core.models import User


async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(User).filter(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()
