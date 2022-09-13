from enum import Enum

from fastapi import APIRouter, Depends

from app.auth.routes import router as auth_router
from app.core.security import get_current_active_user
from app.modules.admin.routes import router as admin_router
from app.modules.system.routes import router as system_router
from app.modules.users.routes import router as users_router

api_router = APIRouter()


def _include_secured_router(router: APIRouter, tags: list[str | Enum]):
    return api_router.include_router(
        router,
        tags=tags,
        dependencies=[
            Depends(get_current_active_user)
        ],  # Todo : Find a solution to factorize differently with scopes system
    )


def _include_unsecured_router(router: APIRouter, tags: list[str | Enum]):
    return api_router.include_router(router, tags=tags)


_include_secured_router(admin_router, tags=["Admin"])
_include_secured_router(users_router, tags=["Users"])
_include_unsecured_router(auth_router, tags=["Auth"])
_include_unsecured_router(system_router, tags=["System"])
