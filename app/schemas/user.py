from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class UserCreate(User):
    password: str
    email: EmailStr
