from enum import Enum

from fastapi import APIRouter, Depends

from app.api.endpoints import admin, auth
from app.core.security import get_current_active_user

api_router = APIRouter()


def _include_secured_router(router: APIRouter, tags: list[str | Enum]):
    return api_router.include_router(
        router, tags=tags, dependencies=[Depends(get_current_active_user)]
    )


def _include_unsecured_router(router: APIRouter, tags: list[str | Enum]):
    return api_router.include_router(router, tags=tags)


_include_secured_router(admin.router, tags=["Admin"])
_include_unsecured_router(auth.router, tags=["Auth"])
