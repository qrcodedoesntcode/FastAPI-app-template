from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str | None = None
    description: str | None = None
