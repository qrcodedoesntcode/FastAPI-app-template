import logging

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from starlette import status

from app.core.config import settings

bearer_scheme = HTTPBearer()

JWT_OPTIONS = {
    "verify_signature": True,
    "verify_aud": False,
    "verify_iat": True,
    "verify_exp": True,
    "verify_nbf": True,
    "verify_iss": False,
    "verify_sub": False,
    "verify_jti": True,
    "verify_at_hash": False,
    "require_aud": False,
    "require_iat": True,
    "require_exp": True,
    "require_nbf": True,
    "require_iss": False,
    "require_sub": True,
    "require_jti": True,
    "require_at_hash": False,
    "leeway": 0,
}


def get_password_hash(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def check_jwt(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    key = settings.JWT_SECRET

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token.scheme.lower() != "bearer":
        raise credentials_exception

    try:
        # Later version: check that the given subject of  the jwt is correct
        jwt.decode(
            token.credentials, key, algorithms=[settings.ALGORITHM], options=JWT_OPTIONS
        )
    except JWTError as e:
        logging.error(e)
        raise credentials_exception

    return True
