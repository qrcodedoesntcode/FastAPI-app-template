from pydantic import BaseModel
from fastapi import Query


class OrmTrue(BaseModel):
    class Config:
        orm_mode = True


# Role classes
class RoleBase(OrmTrue):
    name: str | None = Query(None, min_length=3, max_length=50)
    description: str | None = Query(None, max_length=255)


class RoleCreate(RoleBase):
    pass


class UserRoleBase(OrmTrue):
    username: str | None = None
    roles: list[RoleBase] | None = None


class PermissionBase(OrmTrue):
    scope: str | None = Query(None, min_length=1, max_length=255, property={"description": "The scope of the permission", "placeholder": "admin", "example": "admin"})
    description: str | None = None


class UserPermissionBase(OrmTrue):
    username: str | None = None
    permissions: list[PermissionBase] | None = None
