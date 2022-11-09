from fastapi import APIRouter, Depends, status, Security
from fastapi_pagination import add_pagination
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.params_paginate import Page
from app.db.deps import get_db
from app.modules.core.crud import get_all_roles
from app.modules.core.schema import RoleBase
from app.core.security import get_current_active_user
from app.modules.users.schema import UserSchema


router = APIRouter(prefix="/core")


@router.get(
    "/roles",
    status_code=status.HTTP_200_OK,
    response_model=Page[RoleBase],
    name="Get all roles",
)
async def get_roles(
    db: AsyncSession = Depends(get_db),
) -> AbstractPage:
    return await paginate(db, get_all_roles())


@router.post(
    "/roles",
    status_code=status.HTTP_200_OK,
    name="Create a role",
)
async def create_role() -> AbstractPage:
    pass


@router.get(
    "/roles/{user_id}",
    status_code=status.HTTP_200_OK,
    name="Get specific user roles",
)
async def get_user_roles() -> AbstractPage:
    pass


@router.post(
    "/roles/{user_id}",
    status_code=status.HTTP_200_OK,
    name="Link a specific role to an user",
)
async def link_role_user() -> AbstractPage:
    pass


@router.get(
    "/permissions",
    status_code=status.HTTP_200_OK,
    name="Get all permissions",
)
async def get_permissions() -> AbstractPage:
    pass


@router.post(
    "/permissions",
    status_code=status.HTTP_200_OK,
    name="Create permission",
)
async def link_role_user() -> AbstractPage:
    pass


@router.get(
    "/permissions/{user_id}",
    status_code=status.HTTP_200_OK,
    name="Get specific user permissions",
)
async def get_user_permissions() -> AbstractPage:
    pass


@router.post(
    "/permissions/{user_id}",
    status_code=status.HTTP_200_OK,
    name="Link a permission to an user",
)
async def link_permission_user() -> AbstractPage:
    pass


add_pagination(router)
