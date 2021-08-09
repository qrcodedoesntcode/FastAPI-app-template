from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True


class UserCreate(User):
    password: str
    email: str
