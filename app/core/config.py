from typing import List
from enum import Enum

from pydantic import BaseSettings
from pydantic.networks import AnyHttpUrl


class AppEnvironment(str, Enum):
    PRODUCTION = "production"
    DEV = "development"
    TESTING = "testing"


class Config(BaseSettings):
    """Base configuration."""

    API_V1_STR = "/api/v1"

    APP_VERSION: str = "Unversioned API"
    FASTAPI_ENV: AppEnvironment = AppEnvironment.PRODUCTION

    UVICORN_HOST: str = "0.0.0.0"
    UVICORN_PORT: int = 8000

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str | None = "FastAPI app template"

    DATABASE_USER: str = "app"
    DATABASE_PASSWORD: str = "password"
    DATABASE_URL: str = "127.0.0.1"
    DATABASE_NAME: str = "app"
    DATABASE_PORT: int = 5432
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    LOGGING_LEVEL: str = "INFO"

    ALGORITHM = "HS384"
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_MINUTES = 10_080

    USERS_OPEN_REGISTRATION: bool = True

    JWT_ACCESS_TOKEN_KEY: str
    JWT_REFRESH_TOKEN_KEY: str

    def is_dev(self):
        return self.FASTAPI_ENV == AppEnvironment.DEV

    def is_prod(self):
        return self.FASTAPI_ENV == AppEnvironment.PRODUCTION


settings = Config(_env_file="app/config/.env", _env_file_encoding="utf-8")
