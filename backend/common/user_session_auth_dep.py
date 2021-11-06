from typing import Callable, Any

from fastapi import Depends, Request, Response, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from common.app_settings import app_settings
from common.error_messages import UserManagerErrorMessages, \
    HttpRequestErrorMessages
from services import auth_session_service
from user.interactors import user_interactor

async def authenticate_session(request: Request) -> int:
    session_key = request.cookies.get(app_settings.SESSION_COOKIE_NAME)
    if not session_key:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=HttpRequestErrorMessages.NOT_AUTHENTICATED)
    user_id = await auth_session_service.get_user_email_from_request(request=request)
    if not user_id:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=HttpRequestErrorMessages.NOT_AUTHENTICATED)
    return user_id


async def get_current_user(user_email: str = Depends(authenticate_session)) -> Any:
    user = await user_interactor.get_user_by_email(email=user_email)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=UserManagerErrorMessages.USER_NOT_FOUND)
    return user


async def get_current_active_user(
    request: Request, current_user = Depends(get_current_user),
) -> Any:
    if not current_user.is_active:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=UserManagerErrorMessages.INACTIVE_USER)
    if hasattr(request, "state"):
        request.state.current_user = current_user
    return current_user


def authenticate_user() -> Callable:
    async def check_(_ = Depends(get_current_active_user)) -> None:
        pass

    return check_