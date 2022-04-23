from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session, page: int = 1, per_page: int = 100):
    return db.query(User).limit(per_page).offset((page - 1) * per_page).all()


def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()


def is_active(user: User):
    return user.is_active
