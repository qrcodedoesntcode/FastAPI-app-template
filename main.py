from app.core.logger import logger
from app.app_init import create_app, settings

app = create_app()

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn in reload mode")
    uvicorn.run(
        "main:app",
        host=settings.UVICORN_HOST,
        reload=settings.is_dev(),
        port=settings.UVICORN_PORT,
    )
