from pydantic import BaseModel, Field


class OrmTrue(BaseModel):
    class Config:
        from_attributes = True


# Role classes
class RoleBase(OrmTrue):
    id: int | None = None
    name: str | None = Field(None, min_length=4, max_length=50)
    description: str | None = Field(None, max_length=255)


class RoleUpdate(OrmTrue):
    name: str | None = Field(None, min_length=4, max_length=50)
    description: str | None = Field(None, max_length=255)


class RoleCreate(OrmTrue):
    name: str = Field(..., min_length=4, max_length=50)
    description: str = Field(None, max_length=255)


class UserRoleBase(OrmTrue):
    id: int | None = None
    username: str | None = None
    roles: list[RoleBase] | None = None


class PermissionBase(OrmTrue):
    id: int | None = None
    scope: str | None = Field(None, min_length=4, max_length=255)
    description: str | None = None


class PermissionUpdate(OrmTrue):
    scope: str | None = Field(None, min_length=4, max_length=255)
    description: str | None = None


class PermissionCreate(OrmTrue):
    scope: str = Field(..., min_length=4, max_length=255)
    description: str = Field(..., max_length=255)


class UserPermissionBase(OrmTrue):
    id: int | None = None
    username: str | None = None
    permissions: list[PermissionBase] | None = None


class RolePermissions(RoleBase):
    permissions: list[PermissionBase] | None = None
