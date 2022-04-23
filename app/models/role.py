from sqlalchemy import Column, String, Text

from .database import Base, BaseFeaturesMixin


class Role(Base, BaseFeaturesMixin):
    __tablename__ = "roles"

    name = Column(String(100), index=True)
    description = Column(Text)
