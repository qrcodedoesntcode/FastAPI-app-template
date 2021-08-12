import os
from typing import Optional

from dotenv import load_dotenv


class Config(object):
    """Base configuration."""

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    CONFIG_PATH = os.path.join(ROOT_DIR, "config/.env")

    load_dotenv(CONFIG_PATH)

    def _get(key: str, default: Optional[str] = ""):
        return os.getenv(key, default)

    API_V1_STR = "/api/v1"

    SECRET_KEY = _get("SECRET_KEY", os.urandom(32))

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
    DATABASE_POOL_SIZE = int(_get("DATABASE_POOL_SIZE", "5"))
    DATABASE_MAX_OVERFLOW = int(_get("DATABASE_MAX_OVERFLOW", "10"))

    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
