from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base, BaseFeaturesMixin


class UserRole(Base, BaseFeaturesMixin):
    __tablename__ = "user_roles"

    user_id = Column(
        ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    role_id = Column(
        ForeignKey("roles.id"),
        primary_key=True,
        nullable=False,
    )

    role = relationship("Role")
    user = relationship("User", back_populates="user_role", uselist=False)

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="unique_user_role"),)
