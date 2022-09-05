from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool | None = None


class UserCreate(UserBase):
    password: str
    email: EmailStr


class UserInDBBase(UserBase):
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class UserUpdate(UserInDBBase):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None


class UserSchema(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password: str
