from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import subqueryload

from app.modules.core.models import Role, User, user_role
from app.modules.core.schema import RoleCreate
from app.services import strings


def get_all_roles():
    return select(Role)


async def check_role_exists(db: AsyncSession, role_name: str):
    stmt = select(Role).where(Role.name == role_name)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.ROLE_EXISTS
        )
    return False


async def create_new_role(db: AsyncSession, role: RoleCreate):
    db_role = Role(
        name=role.name,
        description=role.description,
    )
    db.add(db_role)
    await db.commit()
    await db.flush()
    return db_role


async def get_user_roles(db: AsyncSession, user_id: int):
    stmt = (
        select(User)
        .join(user_role)
        .where(
            User.id == user_id,
        )
        .options(subqueryload(User.roles))
    )
    execute = await db.execute(stmt)
    result = execute.scalars().first()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )

    return result
