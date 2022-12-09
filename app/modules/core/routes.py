from fastapi import APIRouter, Depends, Security, status
from fastapi_pagination import add_pagination
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.params_paginate import Page
from app.core.query_factory import check_if_exists, create_entry, get_all_paginate
from app.core.security import get_current_active_user
from app.db.deps import get_db
from app.modules.core.crud import get_user_permission, get_user_roles
from app.modules.core.models import Permission, Role, User
from app.modules.core.schema import (
    PermissionBase,
    RoleBase,
    RoleCreate,
    UserPermissionBase,
    UserRoleBase,
)

router = APIRouter(prefix="/core")


@router.get(
    "/roles",
    status_code=status.HTTP_200_OK,
    response_model=Page[RoleBase],
    name="Get all roles",
)
async def get_roles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(  # noqa
        get_current_active_user, scopes=["admin", "role:read"]
    ),
) -> AbstractPage:
    return await paginate(db, get_all_paginate(Role))


@router.post(
    "/roles",
    status_code=status.HTTP_200_OK,
    response_model=RoleBase,
    name="Create a role",
)
async def create_role(
    role: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(  # noqa
        get_current_active_user, scopes=["admin", "role:create"]
    ),
) -> RoleBase:
    await check_if_exists(db, Role, [Role.name == role.name])
    return await create_entry(db, Role, role)


@router.get(
    "/roles/user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserRoleBase,
    name="Get specific user roles",
)
async def get_specific_user_roles(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(  # noqa
        get_current_active_user, scopes=["admin", "role:read"]
    ),
):
    return await get_user_roles(db, user_id)


@router.post(
    "/roles/user/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRoleBase,
    name="Link a specific role to an user",
)
async def link_role_user():
    pass


@router.get(
    "/permissions",
    status_code=status.HTTP_200_OK,
    response_model=Page[PermissionBase],
    name="Get all permissions",
)
async def get_permissions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(  # noqa
        get_current_active_user, scopes=["admin", "permission:read"]
    ),
) -> AbstractPage:
    return await paginate(db, get_all_paginate(Permission))


@router.post(
    "/permissions",
    status_code=status.HTTP_200_OK,
    response_model=PermissionBase,
    name="Create permission",
)
async def create_permission(
    permission: PermissionBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(  # noqa
        get_current_active_user, scopes=["admin", "permission:create"]
    ),
) -> PermissionBase:
    await check_if_exists(db, Permission, [Permission.scope == permission.scope])
    return await create_entry(db, Permission, permission)


@router.get(
    "/permissions/user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserPermissionBase,
    name="Get specific user permissions",
)
async def get_specific_user_permission(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Security(  # noqa
        get_current_active_user, scopes=["admin", "permission:read"]
    ),
):
    user_permission = await get_user_permission(db, user_id)

    return user_permission


add_pagination(router)
