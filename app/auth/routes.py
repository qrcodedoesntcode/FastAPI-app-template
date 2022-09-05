from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.crud import check_email_is_taken, check_username_is_taken, create_new_user
from app.auth.schema import Message, RefreshToken, Token
from app.core.config import settings
from app.core.security import (
    add_token_to_blacklist,
    check_user_auth,
    generate_access_refresh_token,
    validate_refresh_token,
)
from app.db.deps import get_db
from app.modules.users.schema import UserCreate, UserSchema
from app.services import strings

router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=UserSchema, name="Create an account")
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserSchema:
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.CLOSED_REGISTRATION,
        )
    await check_username_is_taken(db, user.username)
    await check_email_is_taken(db, user.email)

    return await create_new_user(db=db, user=user)


@router.post("/token", response_model=Token, name="Get an access/refresh token")
async def login_for_access_token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    user = await check_user_auth(db, form_data.username, form_data.password)

    return generate_access_refresh_token(user)


@router.post("/refresh_token", response_model=Token, name="Refresh an access token")
async def refresh_token(
    db: AsyncSession = Depends(get_db), form_data: RefreshToken = Depends()
) -> dict:
    user = await validate_refresh_token(db, token=form_data.refresh_token)

    tokens = generate_access_refresh_token(user)

    add_token_to_blacklist(form_data.refresh_token)

    return tokens


@router.post("/logout", name="Logout", response_model=Message)
async def logout() -> dict:
    # Remove access_token/refresh_token from the frontend
    return {"msg": "Successfully logged out"}
