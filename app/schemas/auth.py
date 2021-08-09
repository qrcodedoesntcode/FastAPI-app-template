from typing import Optional

from pydantic import BaseModel


class Login(BaseModel):
    access_token: str
    token_type: str


class LoginData(BaseModel):
    username: Optional[str] = None
