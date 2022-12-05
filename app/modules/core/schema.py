from pydantic import BaseModel


class OrmTrue(BaseModel):
    class Config:
        orm_mode = True


# Role classes
class RoleBase(OrmTrue):
    name: str | None = None
    description: str | None = None


class RoleCreate(RoleBase):
    pass


class UserRoleBase(OrmTrue):
    username: str | None = None
    roles: list[RoleBase] | None = None


class PermissionBase(OrmTrue):
    scope: str | None = None
    description: str | None = None


class UserPermissionBase(OrmTrue):
    permissions: PermissionBase | None = None
