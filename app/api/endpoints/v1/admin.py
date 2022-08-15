from typing import Union

from fastapi import APIRouter, Depends
from fastapi_pagination import add_pagination
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.deps import get_db
from app.core.params_paginate import Page
from app.crud.admin import delete_user_by_user_id, get_all_users, get_user_by_user_id
from app.schemas.user import UserSchema

router = APIRouter(prefix="/admin")
IdType = Union[int, str]


@router.get("/users", response_model=Page[UserSchema], name="Get all users")
async def get_users(
    db: AsyncSession = Depends(get_db),
) -> AbstractPage:
    return await paginate(db, get_all_users())


@router.get(
    "/users/{user_id}",
    response_model=UserSchema,
    name="Get specific user by user_id (id or email)",
)
async def get_specific_user(user_id: IdType, db: AsyncSession = Depends(deps.get_db)):
    return await get_user_by_user_id(db, user_id)


@router.delete(
    "/users/{user_id}",
    name="Delete specific user by user_id (id or email)",
)
async def delete_specific_user(
    user_id: IdType, db: AsyncSession = Depends(deps.get_db)
):
    return await delete_user_by_user_id(db, user_id)


add_pagination(router)
