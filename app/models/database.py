from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import Config

from .mixins import PrimaryKeyMixin, TimestampsMixin


class BaseFeaturesMixin(PrimaryKeyMixin, TimestampsMixin):
    __abstract__ = True


engine = create_engine(
    f"postgresql://{Config.DATABASE_USER}:{Config.DATABASE_PASSWORD}@{Config.DATABASE_URL}/{Config.DATABASE_NAME}",
    pool_size=Config.DATABASE_POOL_SIZE,
    max_overflow=Config.DATABASE_MAX_OVERFLOW,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
