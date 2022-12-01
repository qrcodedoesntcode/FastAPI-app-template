from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.modules.core.models import User, user_role
from app.services import strings


async def get_user_roles(db: AsyncSession, user_id: int):
    stmt = (
        select(User)
        .join(user_role)
        .where(
            User.id == user_id,
        )
        .options(joinedload(User.roles))
    )
    execute = await db.execute(stmt)
    result = execute.scalars().first()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )

    return result
