from fastapi import APIRouter, Security, status

from app.core.security import get_current_active_user
from app.modules.users.schema import UserSchema

router = APIRouter(prefix="/users")


@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    name="Get current user",
)
def profile(
    current_user: UserSchema = Security(get_current_active_user, scopes=["user:read"])
) -> UserSchema:
    return current_user
