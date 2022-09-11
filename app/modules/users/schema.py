from datetime import datetime

from pydantic import BaseModel, EmailStr, constr


class UserProfileBase(BaseModel):
    line1: str | None = None
    line2: str | None = None
    city: str | None = None
    province: str | None = None
    postcode: int | None = None


class UserProfile(UserProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: constr(to_lower=True, min_length=4, max_length=20, strip_whitespace=True)
    email: EmailStr
    is_active: bool | None = None


class UserCreate(UserBase):
    password: constr(min_length=8)
    email: EmailStr


class UserInDBBase(UserBase):
    id: int
    profile: UserProfile | None = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True


class UserUpdate(UserInDBBase):
    username: constr(
        to_lower=True, min_length=4, max_length=20, strip_whitespace=True
    ) | None = None
    email: EmailStr | None = None
    password: constr(min_length=8) | None = None
    is_active: bool | None = None


class UserSchema(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password: constr(min_length=8)
