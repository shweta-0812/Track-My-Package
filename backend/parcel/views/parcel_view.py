from typing import List

from fastapi import APIRouter

from parcel.interactors import parcel_interactor
from parcel.schemas.request import CreateParcel
from parcel.schemas.response import ParcelInDB

router: APIRouter = APIRouter()


@router.get(
    "/", response_model=List[ParcelInDB],
)
async def get_parcels_list():
    return await parcel_interactor.get_parcels_list()


@router.get("/{id}/", response_model=ParcelInDB)
async def get_parcel(id: int):
    return await parcel_interactor.get_parcel(id=id)


@router.get("/latest/", response_model=ParcelInDB)
async def get_latest_parcel():
    return await parcel_interactor.get_latest_parcel()


@router.post("/", response_model=ParcelInDB)
async def create_parcel(create_parcel: CreateParcel):
    return await parcel_interactor.create_parcel(create_parcel=create_parcel)


@router.patch("/{id}/", response_model=ParcelInDB)
async def update_parcel(id: int):
    return await parcel_interactor.get_parcel(id=id)
