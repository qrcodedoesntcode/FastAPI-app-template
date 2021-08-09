from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class UserCreate(User):
    password: str
    email: str
