import os
from typing import List, Optional

from pydantic import BaseSettings
from pydantic.networks import AnyHttpUrl


class Config(BaseSettings):
    """Base configuration."""

    API_V1_STR = "/api/v1"

    SECRET_KEY: str = str(os.urandom(32))

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: Optional[str] = "FastAPI app template"

    DATABASE_USER: str = "app"
    DATABASE_PASSWORD: str = "password"
    DATABASE_URL: str = "127.0.0.1"
    DATABASE_NAME: str = "app"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Config(_env_file="config/.env", _env_file_encoding="utf-8")
