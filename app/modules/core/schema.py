from fastapi import Query
from pydantic import BaseModel


class OrmTrue(BaseModel):
    class Config:
        from_attributes = True


# Role classes
class RoleBase(OrmTrue):
    id: int | None = None
    name: str | None = Query(None, min_length=3, max_length=50)
    description: str | None = Query(None, max_length=255)


class RoleUpdate(OrmTrue):
    name: str | None = Query(None, min_length=3, max_length=50)
    description: str | None = Query(None, max_length=255)


class RoleCreate(OrmTrue):
    name: str
    description: str


class UserRoleBase(OrmTrue):
    id: int | None = None
    username: str | None = None
    roles: list[RoleBase] | None = None


class PermissionBase(OrmTrue):
    id: int | None = None
    scope: str | None = Query(
        None,
        min_length=1,
        max_length=255,
        property={
            "description": "The scope of the permission",
            "placeholder": "admin",
            "example": "admin",
        },
    )
    description: str | None = None


class PermissionUpdate(OrmTrue):
    scope: str | None = Query(
        None,
        min_length=1,
        max_length=255,
        property={
            "description": "The scope of the permission",
            "placeholder": "admin",
            "example": "admin",
        },
    )
    description: str | None = None


class PermissionCreate(OrmTrue):
    scope: str
    description: str


class UserPermissionBase(OrmTrue):
    id: int | None = None
    username: str | None = None
    permissions: list[PermissionBase] | None = None


class RolePermissions(RoleBase):
    permissions: list[PermissionBase] | None = None
