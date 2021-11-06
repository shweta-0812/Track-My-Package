from common import base_repo
from common.app_settings import app_settings
from user.model import USER_MODEL, User


async def create_user(user: User):
    return await base_repo.create(klass=USER_MODEL, doc_data=user.dict())


async def does_index_exists() -> bool:
    return await base_repo.does_index_exists(klass=USER_MODEL)


async def create_index():
    return await base_repo.create_index(
        klass=USER_MODEL,
        settings=app_settings.DEFAULT_ES_INDEX_SETTINGS,
        mappings={
            "properties": {
                "id": {"type": "integer"},
                "email": {"type": "text"},
                "first_name": {"type": "text"},
                "last_name": {"type": "text"},
                "status": {"type": "integer"},
                "date": {"type": "integer"},
                "created_at": {"type": "integer"},
                "updated_at": {"type": "integer"},
            }
        },
    )


async def delete_index():
    return await base_repo.delete_index(klass=USER_MODEL)


async def get_users():
    return await base_repo.get_all(klass=USER_MODEL)


async def get_latest_user():
    return await base_repo.get_latest(klass=USER_MODEL)


async def count(email: str = None):
    count_filter_kwargs = locals().copy()
    return await base_repo.count(klass=USER_MODEL, filters=count_filter_kwargs)


async def get(id: str = None):
    return await base_repo.get(klass=USER_MODEL, id=id)


async def _filter(email: str = None):
    filter_kwargs = locals().copy()
    return await base_repo._filter(klass=USER_MODEL, filters=filter_kwargs)


async def update(id: str, status: int = None, email: str = None):
    update_kwargs = locals().copy()
    return await base_repo.update(klass=USER_MODEL, **update_kwargs)


async def create(email: str = None):
    return await base_repo.create(klass=USER_MODEL)


async def delete(id: str = None):
    return await base_repo.delete(klass=USER_MODEL, id=id)
