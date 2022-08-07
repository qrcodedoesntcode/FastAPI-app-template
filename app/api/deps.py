from app.models.database import async_session


async def get_db():
    async with async_session() as db:
        yield db
