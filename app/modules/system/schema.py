from pydantic import BaseModel


class Root(BaseModel):
    name: str
    version: str


class Health(BaseModel):
    msg: str
