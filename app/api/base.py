from enum import Enum

from fastapi import APIRouter, Depends

from app.api.endpoints import admin, login
from app.core.security import check_jwt

api_router = APIRouter()


def _include_secured_router(router: APIRouter, tags: list[str | Enum]):
    return api_router.include_router(
        router, tags=tags, dependencies=[Depends(check_jwt)]
    )


def _include_unsecured_router(router: APIRouter, tags: list[str | Enum]):
    return api_router.include_router(router, tags=tags)


_include_secured_router(admin.router, tags=["Admin"])
_include_unsecured_router(login.router, tags=["Login"])
