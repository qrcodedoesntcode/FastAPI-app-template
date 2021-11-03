from sqlalchemy import Boolean, Column, String

from .database import Base, BaseFeaturesMixin
from sqlalchemy.orm import relationship


class User(Base, BaseFeaturesMixin):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    user_role = relationship("UserRole", back_populates="user", uselist=False)
