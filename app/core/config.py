import os


class Config(object):
    """Base configuration."""

    API_V1_STR = "/api/v1"

    SECRET_KEY = os.getenvb(b"SECRET_KEY")
    if not SECRET_KEY:
        SECRET_KEY = os.urandom(32)

    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

    SERVER_NAME = os.getenv("SERVER_NAME")
    SERVER_HOST = os.getenv("SERVER_HOST")
    BACKEND_CORS_ORIGINS = os.getenv(
        "BACKEND_CORS_ORIGINS"
    )  # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:8080"
    PROJECT_NAME = os.getenv("PROJECT_NAME", "FastAPI app template")

    DATABASE_USER = os.getenv("DATABASE_USER", "app")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_URL = os.getenv("DATABASE_URL", "127.0.0.1")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "app")
