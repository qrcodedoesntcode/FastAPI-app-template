import os
from typing import Optional


class Config(object):
    """Base configuration."""

    def _get(key: str, default: Optional[str] = ""):
        return os.getenv(key, default)

    API_V1_STR = "/api/v1"

    SECRET_KEY = _get("SECRET_KEY")
    if not SECRET_KEY:
        SECRET_KEY = os.urandom(32)

    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

    SERVER_NAME = _get("SERVER_NAME")
    SERVER_HOST = _get("SERVER_HOST")
    BACKEND_CORS_ORIGINS = _get(
        "BACKEND_CORS_ORIGINS"
    )  # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:8080"
    PROJECT_NAME = _get("PROJECT_NAME", "FastAPI app template")

    DATABASE_USER = _get("DATABASE_USER", "app")
    DATABASE_PASSWORD = _get("DATABASE_PASSWORD", "password")
    DATABASE_URL = _get("DATABASE_URL", "127.0.0.1")
    DATABASE_NAME = _get("DATABASE_NAME", "app")
    SECRET_KEY = (
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # tmp
    )
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
