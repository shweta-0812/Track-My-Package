from fastapi import APIRouter
from staff_user.interactors import staff_user_interactor

router: APIRouter = APIRouter()


@router.get("/list-doc/")
async def get_doc_list(index: str):
    return await staff_user_interactor.get_docs_list(index=index)


@router.get("/cat-indices/")
async def cat_indices():
    return await staff_user_interactor.cat_indices()


@router.get("/create-index/")
async def create_index(index: str):
    return await staff_user_interactor.create_index(index=index)


@router.get("/delete-index/")
async def delete_index(index: str):
    return await staff_user_interactor.delete_index(index=index)


@router.get("/check-index/")
async def check_index(index: str):
    return await staff_user_interactor.does_index_exists(index=index)


@router.get("/get-latest-doc/")
async def get_latest_parcel(index: str):
    return await staff_user_interactor.get_latest_parcel(index=index)


@router.get("/get-doc/{id}/")
async def get_parcel(index: str, id: int):
    return await staff_user_interactor.get_doc(index=index, id=id)
