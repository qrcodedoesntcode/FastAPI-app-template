from sqlalchemy.future import select

from app.modules.core.models import Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


def get_all_roles():
    return select(Role)
