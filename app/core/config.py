from enum import Enum
from typing import List

from pydantic.networks import AnyHttpUrl
from pydantic_settings import BaseSettings


class AppEnvironment(str, Enum):
    PRODUCTION = "production"
    DEV = "development"
    TESTING = "testing"


class Config(BaseSettings):
    """
    Base configuration.
    """

    API_V1_STR: str = "/api/v1"

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

    REDIS_CONNECTION: bool = False
    REDIS_URL: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_SOCKET_TIMEOUT: int = 5

    SENTRY_ENABLED: bool | None = False
    SENTRY_DSN: str | None = None
    SENTRY_ENV: str | None = "dev"

    LOGGING_LEVEL: str = "INFO"
    SQL_VERBOSE_LOGGING: bool = False

    ALGORITHM: str = "HS384"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10_080

    EMAIL_TOKEN_EXPIRE_HOURS: int = 24
    EMAIL_SENDER: str = "fastapi@example.com"
    EMAIL_SENDER_NAME: str = "FastAPI app template"

    MAILJET_API_KEY: str | None = None
    MAILJET_API_SECRET: str | None = None

    USERS_OPEN_REGISTRATION: bool = True

    JWT_ACCESS_TOKEN_KEY: str
    JWT_REFRESH_TOKEN_KEY: str

    def is_dev(self) -> bool:
        return self.FASTAPI_ENV == AppEnvironment.DEV

    def is_prod(self) -> bool:
        return self.FASTAPI_ENV == AppEnvironment.PRODUCTION


settings = Config(_env_file=".env", _env_file_encoding="utf-8")
