from fastapi import APIRouter, Depends, status

from app.core.security import get_current_active_user
from app.modules.users.schema import UserSchema

router = APIRouter(prefix="/users")


@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    name="Get current user",
)
def profile(current_user: UserSchema = Depends(get_current_active_user)) -> UserSchema:
    return current_user
