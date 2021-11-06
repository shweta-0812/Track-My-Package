from uuid import UUID

from fastapi import APIRouter, Request, Depends
from starlette.responses import JSONResponse

from common.user_session_auth_dep import get_current_active_user
from common.schema import Success
from services import auth_session_service
from services.auth_session_service import cookie
from user.interactors import user_interactor
from user.schemas.request import CreateUser, UpdateUser
from user.schemas.response import UserInDB

router: APIRouter = APIRouter()


# @router.get(
#     "/", response_model=List[UserInDB],
# )
# async def get_users_list():
#     return await user_interactor.get_users_list()


@router.get("/me/", response_model=UserInDB)
async def get_user_me(current_user=Depends(get_current_active_user)):
    return current_user


@router.post("/", response_model=UserInDB)
async def create_user(create_user: CreateUser):
    return await user_interactor.create_user(create_user=create_user)


@router.patch("/me/", response_model=UserInDB)
async def update_user_me(
    update_user: UpdateUser, current_user=Depends(get_current_active_user)
):
    user_update_data = update_user.dict(exclude_unset=True, exclude_none=True)
    if user_update_data:
        updated_user = await user_interactor.update_user(
            current_user=current_user, **user_update_data
        )
        return updated_user
    return current_user


@router.post("/logout/", response_model=Success)
async def logout(session_id: UUID = Depends(cookie)) -> JSONResponse:
    response = await auth_session_service.delete_session_for_user(session_id=session_id)
    return response
