from fastapi import APIRouter, Security, status

from app.core.security import get_current_active_user
from app.modules.users.schema import UserSchemaProfile

router = APIRouter(prefix="/users")


@router.get(
    "/current",
    status_code=status.HTTP_200_OK,
    response_model=UserSchemaProfile,
    name="Get current user",
)
def get_current_user(
    current_user: UserSchemaProfile = Security(get_current_active_user),
) -> UserSchemaProfile:
    return current_user
