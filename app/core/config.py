import base64
import os
from typing import Any, List, Optional

from pydantic import BaseSettings, validator
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

    ALGORITHM = "HS384"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    SECRET_KEY: str

    JWT_KEY: str
    JWT_SECRET: str | None

    @validator("JWT_SECRET")
    def build_jwt_secret(cls, v: str | None, values: dict[str, Any]):
        if v:
            return v

        jwt_key = values.get("JWT_KEY")

        if not jwt_key:
            return ""

        return base64.urlsafe_b64decode(jwt_key)


settings = Config(_env_file="config/.env", _env_file_encoding="utf-8")
