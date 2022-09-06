import uuid
from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.schema import TokenData
from app.core.config import settings
from app.core.logger import logger
from app.db.deps import get_db
from app.modules.admin.crud import get_user_by_username
from app.modules.users.schema import UserSchema
from app.services import strings
from app.services.storage import storage

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")


JWT_OPTIONS = {
    "verify_signature": True,
    "verify_aud": False,
    "verify_iat": True,
    "verify_exp": True,
    "verify_nbf": False,
    "verify_iss": True,
    "verify_sub": True,
    "verify_jti": True,
    "verify_at_hash": False,
    "require_aud": False,
    "require_iat": True,
    "require_exp": True,
    "require_nbf": False,
    "require_iss": True,
    "require_sub": True,
    "require_jti": True,
    "require_at_hash": False,
    "leeway": 0,
}


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


async def check_user_auth(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=strings.INCORRECT_USER_PASSWORD,
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not user:
        raise credentials_error
    if not verify_password(password, user.password):
        raise credentials_error
    logger.info(f"Authenticating user {username}")
    return user


def create_jwt_token(
    data: dict, expires_delta: timedelta | None = None, scope: str = "access_token"
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    iat = datetime.utcnow()
    iss = settings.PROJECT_NAME
    jti = str(uuid.uuid4())

    jwt_key = (
        settings.JWT_ACCESS_TOKEN_KEY
        if scope == "access_token"
        else settings.JWT_REFRESH_TOKEN_KEY
    )
    to_encode.update(
        {"exp": expire, "iat": iat, "iss": iss, "jti": jti, "scope": scope}
    )
    encoded_jwt = jwt.encode(to_encode, jwt_key, algorithm=settings.ALGORITHM)
    logger.debug(f"Creating {scope} for user {data['sub']}")
    return encoded_jwt


async def check_jwt(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    scope: str = Query(default="access_token", include_in_schema=False),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=strings.COULD_NOT_VALIDATE_CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        jwt_key = (
            settings.JWT_ACCESS_TOKEN_KEY
            if scope == "access_token"
            else settings.JWT_REFRESH_TOKEN_KEY
        )
        payload = jwt.decode(
            token,
            jwt_key,
            algorithms=[settings.ALGORITHM],
            options=JWT_OPTIONS,
        )
        jti: str = payload.get("jti")
        username: str = payload.get("sub")
        if jti in storage:
            logger.debug(f"{jti} is in blacklist")
            raise credentials_exception
        if username is None:
            logger.debug("sub is None")
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: UserSchema = Depends(check_jwt),
) -> UserSchema:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=strings.COULD_NOT_VALIDATE_CREDENTIALS,
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INACTIVE_USER
        )
    return current_user


def validate_refresh_token(db: AsyncSession, token: str = Depends(oauth2_scheme)):
    return check_jwt(db, token, "refresh_token")


def add_token_to_blacklist(token: str, scope: str = "refresh_token") -> None:
    """
    Add token to the blacklist.
    Added the possibility to blacklist a token by scope (refresh_token, access_token).
    """
    jwt_key = (
        settings.JWT_ACCESS_TOKEN_KEY
        if scope == "access_token"
        else settings.JWT_REFRESH_TOKEN_KEY
    )
    payload = jwt.decode(
        token,
        jwt_key,
        algorithms=[settings.ALGORITHM],
        options=JWT_OPTIONS,
    )
    jti = payload.get("jti")
    exp = payload.get("exp")
    storage.set_key(jti, exp)
    logger.info(f"Adding {jti} (expiring {exp}) to blacklist")


def generate_access_refresh_token(user) -> dict:
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

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
