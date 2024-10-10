from fastapi import APIRouter, Depends, status
from fastapi_users import models, BaseUserManager
from user.user_manager import get_user_manager
from fastapi import Request
from fastapi_auth.auth import get_current_active_user


router = APIRouter()


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The user does not exist.",
        },
    },
)
async def delete_own_account(
    request: Request,
    user: models.UP = Depends(get_current_active_user),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    await user_manager.delete(user, request=request)
    return None
