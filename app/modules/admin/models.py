from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import BaseFeaturesMixin


class User(Base, BaseFeaturesMixin):
    __tablename__ = "adm_user"

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)

    # Relationship
    profile = relationship(
        "Profile",
        back_populates="user",
        cascade="all,delete",
        uselist=False,
        lazy=False,
    )


class Profile(Base, BaseFeaturesMixin):
    __tablename__ = "adm_profile"

    line1 = Column(String(255))
    line2 = Column(String(255))
    city = Column(String(255))
    province = Column(String(255))
    postcode = Column(String(255))
    user_id = Column(Integer, ForeignKey("adm_user.id"))

    # Relationship
    user = relationship("User", back_populates="profile", lazy=False)
