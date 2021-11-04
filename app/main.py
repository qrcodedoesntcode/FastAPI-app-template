from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.base import router as api_router

from .core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# CORS
origins = []

# Set all CORS enabled origins : adding security between Backend and Frontend
if settings.BACKEND_CORS_ORIGINS:
    origins_raw = settings.BACKEND_CORS_ORIGINS.split(",")

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

app.include_router(api_router, prefix=settings.API_V1_STR)
