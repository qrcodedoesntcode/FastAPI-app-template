from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schema import Message, RefreshToken, Token
from app.core.config import settings
from app.core.query_factory import check_if_exists, create_entry
from app.core.security import (
    add_token_to_blacklist,
    check_user_auth,
    generate_access_refresh_token,
    get_password_hash,
    validate_refresh_token,
)
from app.db.deps import get_db
from app.modules.core.models import Profile, User
from app.modules.users.schema import UserCreate, UserSchema
from app.services import strings

router = APIRouter(prefix="/auth")


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchema,
    name="Create an account",
)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserSchema:
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.CLOSED_REGISTRATION,
        )
    await check_if_exists(db, User, [User.username == user.username])
    await check_if_exists(db, User, [User.email == user.email])

    data_in = {
        "username": user.username,
        "email": user.email,
        "password": get_password_hash(user.password),
        "is_active": user.is_active,
    }

    user = await create_entry(db, User, data_in)
    await create_entry(db, Profile, {"user_id": user.id})

    return user


@router.post(
    "/token",
    status_code=status.HTTP_201_CREATED,
    response_model=Token,
    name="Get an access/refresh token",
)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    user = await check_user_auth(db, form_data.username, form_data.password)

    return generate_access_refresh_token(user, form_data)


@router.post(
    "/refresh_token",
    status_code=status.HTTP_201_CREATED,
    response_model=Token,
    name="Refresh an access token",
)
async def refresh_token(
    db: AsyncSession = Depends(get_db), form_data: RefreshToken = Depends()
) -> dict:
    user = await validate_refresh_token(db, token=form_data.refresh_token)

    tokens = generate_access_refresh_token(user, form_data)

    add_token_to_blacklist(form_data.refresh_token)

    return tokens


@router.post(
    "/logout", status_code=status.HTTP_200_OK, name="Logout", response_model=Message
)
async def logout() -> dict:
    # Remove access_token/refresh_token from the frontend
    return {"msg": "Successfully logged out"}
