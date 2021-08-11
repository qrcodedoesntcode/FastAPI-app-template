from fastapi import APIRouter

from app.api import auth, user, admin

router = APIRouter()

router.include_router(auth.router, tags=["Authentication"])
router.include_router(admin.router, tags=["Admin"])
router.include_router(user.router, tags=["Users"])
