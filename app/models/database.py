from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

from .mixins import PrimaryKeyMixin, TimestampsMixin


class BaseFeaturesMixin(PrimaryKeyMixin, TimestampsMixin):
    __abstract__ = True


engine = create_async_engine(
    f"""postgresql+asyncpg://
    {settings.DATABASE_USER}:
    {settings.DATABASE_PASSWORD}@
    {settings.DATABASE_URL}/
    {settings.DATABASE_NAME}""",
    pool_pre_ping=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    future=True,
)
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True,
    autoflush=False,
)

Base = declarative_base()
