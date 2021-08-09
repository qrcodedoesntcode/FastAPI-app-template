from fastapi import APIRouter

from app.api import auth, user

router = APIRouter()

router.include_router(auth.router, tags=["Authentication"])
router.include_router(user.router, tags=["Users"])
