from .database import Base, BaseFeaturesMixin

from sqlalchemy import Column, String, Text, Integer


class Role(Base, BaseFeaturesMixin):
    __tablename__ = "roles"

    name = Column(String(100), index=True)
    description = Column(Text)
