from fastapi import APIRouter
from parcel.interactors import parcel_interactor
from parcel.schema import CreateParcel

router: APIRouter = APIRouter()


@router.get("/")
async def get_parcels_list():
    return await parcel_interactor.get_parcels_list()


@router.get("/cat-indices/")
async def cat_indices():
    return await parcel_interactor.cat_indices()


@router.get("/create-index/")
async def create_index():
    return await parcel_interactor.create_index()


@router.get("/delete-index/")
async def delete_index():
    return await parcel_interactor.delete_index()


@router.get("/check-index/")
async def check_index():
    return await parcel_interactor.does_index_exists()


@router.get("/latest/")
async def get_latest_parcel():
    return await parcel_interactor.get_latest_parcel()


@router.post("/")
async def create_parcel(create_parcel: CreateParcel):
    return await parcel_interactor.create_parcel(create_parcel=create_parcel)


@router.patch("/{id}/")
async def update_parcel():
    return {}


@router.get("/{id}/")
async def get_parcel():
    return {}
