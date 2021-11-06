from common import base_repo
from parcel.models import Parcel, PARCEL_MODEL


async def create_parcel(parcel: Parcel):
    return await base_repo.create(klass=PARCEL_MODEL, doc_data=parcel.dict())


async def does_index_exists() -> bool:
    return await base_repo.does_index_exists(klass=PARCEL_MODEL)


async def create_index():
    return await base_repo.create_index(
        klass=PARCEL_MODEL,
        settings={"number_of_shards": 3, "number_of_replicas": 2},
        mappings={
            "properties": {
                "id": {"type": "integer"},
                "awn_number": {"type": "text"},
                "delivery_partner": {"type": "integer"},
                "status": {"type": "integer"},
                "date": {"type": "integer"},
                "created_at": {"type": "integer"},
                "updated_at": {"type": "integer"},
            }
        },
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
