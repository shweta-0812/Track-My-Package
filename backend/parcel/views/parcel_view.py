from typing import List

from fastapi import APIRouter, Depends

from parcel.interactors import parcel_interactor
from parcel.schemas.request import CreateParcel
from parcel.schemas.response import Parcel

router: APIRouter = APIRouter()


@router.get(
    "/",
    response_model=List[Parcel],
)
async def get_parcels_list():
    return await parcel_interactor.get_parcels_list()


@router.get("/{id}/", response_model=Parcel)
async def get_parcel(id: int):
    return await parcel_interactor.get_parcel(id=id)


@router.get("/latest/", response_model=Parcel)
async def get_latest_parcel():
    return await parcel_interactor.get_latest_parcel()


@router.post("/", response_model=Parcel)
async def create_parcel(create_parcel: CreateParcel):
    return await parcel_interactor.create_parcel(create_parcel=create_parcel)


@router.patch("/{id}/", response_model=Parcel)
async def update_parcel(id: int):
    return await parcel_interactor.get_parcel(id=id)
