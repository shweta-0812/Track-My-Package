from fastapi import APIRouter

from parcel.urls import parcel_router


api_v1_base_router = APIRouter()

session_authenticated_api_router = APIRouter()
token_authenticated_api_router = APIRouter()
non_authenticated_api_router = APIRouter()
staff_authenticated_api_router = APIRouter()

session_authenticated_api_router.include_router(parcel_router)

api_v1_base_router.include_router(
    # session_authenticated_api_router, dependencies=[Depends(authenticate_user())]
    session_authenticated_api_router
)
api_v1_base_router.include_router(non_authenticated_api_router)
api_v1_base_router.include_router(token_authenticated_api_router)
api_v1_base_router.include_router(
    # staff_authenticated_api_router, dependencies=[Depends(authenticate_staff_user())]
    staff_authenticated_api_router
)
