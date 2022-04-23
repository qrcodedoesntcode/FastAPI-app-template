from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate


def check_username_is_taken(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def check_email_is_taken(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_new_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
        is_active=user.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
