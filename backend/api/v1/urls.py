from fastapi import APIRouter, Depends

from common.user_session_auth_dep import authenticate_user
from parcel.urls import parcel_router
from user.views.user_token_view import router as user_token_auth_router


api_v1_base_router = APIRouter()

# initialize
non_authenticated_api_router = APIRouter()
user_session_authenticated_api_router = APIRouter()
staff_authenticated_api_router = APIRouter()

# include
non_authenticated_api_router.include_router(user_token_auth_router)
user_session_authenticated_api_router.include_router(parcel_router)


# set in base router
api_v1_base_router.include_router(
    user_session_authenticated_api_router, dependencies=[Depends(authenticate_user())]
)
api_v1_base_router.include_router(non_authenticated_api_router)

# api_v1_base_router.include_router(
#     staff_authenticated_api_router, dependencies=[Depends(authenticate_staff_user())]
# )
