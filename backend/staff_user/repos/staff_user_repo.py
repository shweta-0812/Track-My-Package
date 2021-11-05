from typing import Any, Dict

from common import base_repo


async def does_index_exists() -> bool:
    return await base_repo.does_index_exists(klass="parcel")


async def create_index(index: str, mappings: Dict[Any, Any], settings: Dict[Any, Any]):
    return await base_repo.create_index(klass=index,
                                        settings=settings,
                                        mappings=mappings)


async def delete_index(index: str):
    return await base_repo.delete_index(klass="parcel")


async def cat_indices():
    return await base_repo.cat_indices()


async def get_doc(index: str, id: int):
    return await base_repo.get(klass=index, id=id)

async def get_latest_doc(index: str):
    return await base_repo.get_latest(klass=index)
