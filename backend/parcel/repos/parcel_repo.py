from common import base_repo
from common.app_settings import app_settings
from parcel.model import Parcel, PARCEL_MODEL, PARCEL_ES_INDEX_DOC_MAPPINGS


async def create_parcel(parcel: Parcel):
    return await base_repo.create(klass=PARCEL_MODEL, doc_data=parcel.dict())


async def does_index_exists() -> bool:
    return await base_repo.does_index_exists(klass=PARCEL_MODEL)


async def create_index():
    return await base_repo.create_index(
        klass=PARCEL_MODEL,
        settings=app_settings.DEFAULT_ES_INDEX_SETTINGS,
        mappings=PARCEL_ES_INDEX_DOC_MAPPINGS
    )


async def delete_index():
    return await base_repo.delete_index(klass=PARCEL_MODEL)


async def cat_indices():
    return await base_repo.cat_indices()


async def get_parcel(id: int):
    return await base_repo.get(klass=PARCEL_MODEL, id=id)


async def get_parcels():
    return await base_repo.get_all(klass=PARCEL_MODEL)


async def get_latest_parcel():
    return await base_repo.get_latest(klass=PARCEL_MODEL)
