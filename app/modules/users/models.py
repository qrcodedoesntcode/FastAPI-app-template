from sqlalchemy import Boolean, Column, String

from app.db.database import Base, BaseFeaturesMixin


class User(Base, BaseFeaturesMixin):
    __tablename__ = "user"

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
