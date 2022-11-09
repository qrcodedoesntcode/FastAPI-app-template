from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.deps import pivot_table, reference_col
from app.db.mixins import BaseFeaturesMixin

# Association/Pivot tables
user_role = pivot_table(
    "cre_user_role",
    {"table": "cre_user", "ondelete": "CASCADE"},
    {"table": "cre_role", "ondelete": "CASCADE"},
)

role_permission = pivot_table(
    "cre_role_permission",
    {"table": "cre_role", "ondelete": "CASCADE"},
    {"table": "cre_permission", "ondelete": "CASCADE"},
)


class User(Base, BaseFeaturesMixin):
    __tablename__ = "cre_user"

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
    roles = relationship("Role", secondary=user_role)


class Profile(Base, BaseFeaturesMixin):
    __tablename__ = "cre_profile"

    line1 = Column(String(255))
    line2 = Column(String(255))
    city = Column(String(255))
    province = Column(String(255))
    postcode = Column(String(255))
    user_id = reference_col(User.__tablename__)

    # Relationship
    user = relationship("User", back_populates="profile", lazy=False)


class Role(Base, BaseFeaturesMixin):
    __tablename__ = "cre_role"

    name = Column(String(50), unique=True)
    description = Column(String(255))

    # Relationship
    # users = relationship("User", secondary=user_role)
    permissions = relationship("Permission", secondary=role_permission)


class Permission(Base, BaseFeaturesMixin):
    __tablename__ = "cre_permission"

    scope = Column(String(50), unique=True, index=True)
    description = Column(String(255))
