from typing import Union

from fastapi import APIRouter, Depends, Security, status
from fastapi_pagination import add_pagination
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.params_paginate import Page
from app.core.schema import DefaultResponse
from app.core.security import get_current_active_user
from app.db.deps import get_db
from app.modules.admin.crud import (
    delete_user_by_user_id,
    get_all_users,
    get_user_by_user_id,
)
from app.modules.users.schema import UserSchema

router = APIRouter(prefix="/admin")
IdType = Union[int, str]


@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=Page[UserSchema],
    name="Get all users",
)
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user: UserSchema = Security(  # noqa
        get_current_active_user, scopes=["admin"]
    ),
) -> AbstractPage:
    return await paginate(db, get_all_users())


@router.get(
    "/users/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    name="Get specific user by user_id (id or email)",
)
async def get_specific_user(
    user_id: IdType,
    db: AsyncSession = Depends(get_db),
    current_user: UserSchema = Security(  # noqa
        get_current_active_user, scopes=["admin"]
    ),
):
    return await get_user_by_user_id(db, user_id)


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=DefaultResponse,
    name="Delete specific user by user_id (id or email)",
)
async def delete_specific_user(
    user_id: IdType,
    db: AsyncSession = Depends(get_db),
    current_user: UserSchema = Security(  # noqa
        get_current_active_user, scopes=["admin", "user:delete"]
    ),
):
    return await delete_user_by_user_id(db, user_id)


add_pagination(router)
