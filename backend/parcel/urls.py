from fastapi import APIRouter

from parcel.views import parcel_view

parcel_router = APIRouter()

parcel_router.include_router(
    parcel_view.router, prefix="/parcel", tags=["parcel"],
)

