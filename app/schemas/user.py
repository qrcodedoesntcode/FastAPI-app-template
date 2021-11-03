from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = None


class UserCreate(UserBase):
    password: str
    email: EmailStr


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password: str
