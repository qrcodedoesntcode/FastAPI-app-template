from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api import user
from .core.config import Config

app = FastAPI(title=Config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")

# CORS
origins = []

# Set all CORS enabled origins : adding security between Backend and Frontend
if Config.BACKEND_CORS_ORIGINS:
    origins_raw = Config.BACKEND_CORS_ORIGINS.split(",")

    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.include_router(user.router, prefix=Config.API_V1_STR)
