from fastapi import APIRouter

from user.views import user_view

user_router = APIRouter()

user_router.include_router(
    user_view.router, prefix="/user", tags=["user"],
)

