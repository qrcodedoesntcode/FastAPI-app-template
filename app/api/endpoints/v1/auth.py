from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import (
    authenticate_user,
    create_jwt_token,
    validate_refresh_token,
)
from app.crud.auth import check_email_is_taken, check_username_is_taken, create_new_user
from app.resources import strings
from app.schemas.auth import RefreshToken, Token
from app.schemas.user import UserCreate, UserSchema

router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=UserSchema, name="Create an account")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.CLOSED_REGISTRATION,
        )
    if await check_username_is_taken(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN,
        )

    if await check_email_is_taken(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )
    return await create_new_user(db=db, user=user)


def _generate_access_refresh_token(user):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_jwt_token(
        data={"sub": user.username},
        expires_delta=refresh_token_expires,
        scope="refresh_token",
    )

    return access_token, refresh_token


@router.post("/token", response_model=Token, name="Get an access/refresh token")
async def login_for_access_token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=strings.INCORRECT_USER_PASSWORD,
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token = _generate_access_refresh_token(user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh_token", response_model=Token, name="Refresh an access token")
async def refresh_token(
    db: AsyncSession = Depends(get_db), form_data: RefreshToken = Depends()
):
    user = await validate_refresh_token(db, token=form_data.refresh_token)

    access_token, refresh_token = _generate_access_refresh_token(user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
