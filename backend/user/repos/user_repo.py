from common import base_repo
from user.model import USER_MODEL


async def count(email: str = None):
    count_filter_kwargs = locals().copy()
    return await base_repo.count(klass=USER_MODEL, filters=count_filter_kwargs)


async def get(id: str = None):
    return await base_repo.get(klass=USER_MODEL, id=id)


async def _filter(email: str = None):
    filter_kwargs = locals().copy()
    return await base_repo._filter(klass=USER_MODEL, filters=filter_kwargs)


async def update(id:str, status:int = None, email: str = None):
    update_kwargs = locals().copy()
    return await base_repo.update(klass=USER_MODEL, **update_kwargs)


async def create(email: str = None):
    return await base_repo.create(klass=USER_MODEL)


async def delete(id: str = None):
    return await base_repo.delete(klass=USER_MODEL, id=id)
