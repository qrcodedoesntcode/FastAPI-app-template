import base64
import os
from typing import Any, List

from pydantic import BaseSettings, validator
from pydantic.networks import AnyHttpUrl


class Config(BaseSettings):
    """Base configuration."""

    API_V1_STR = "/api/v1"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str | None = "FastAPI app template"

    DATABASE_USER: str = "app"
    DATABASE_PASSWORD: str = "password"
    DATABASE_URL: str = "127.0.0.1"
    DATABASE_NAME: str = "app"
    DATABASE_PORT: int = 5432
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    ALGORITHM = "HS384"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    USERS_OPEN_REGISTRATION: bool = True

    JWT_KEY: str


settings = Config(_env_file="app/config/.env", _env_file_encoding="utf-8")
