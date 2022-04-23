from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

from .mixins import PrimaryKeyMixin, TimestampsMixin


class BaseFeaturesMixin(PrimaryKeyMixin, TimestampsMixin):
    __abstract__ = True


engine = create_engine(
    f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_URL}/{settings.DATABASE_NAME}",
    pool_pre_ping=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
