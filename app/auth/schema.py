from pydantic import BaseModel, constr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    username: constr(
        to_lower=True, min_length=4, max_length=20, strip_whitespace=True
    ) | None = None


class Message(BaseModel):
    msg: str
