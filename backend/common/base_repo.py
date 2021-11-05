from typing import Any, Optional

from common import base_repo_es_wrapper


async def create(klass: str, doc_data=Any, doc_version=1):
    return await base_repo_es_wrapper.create(
        index=klass, doc_data=doc_data, doc_version=doc_version
    )


async def cat_indices(klass: Optional[str] = None):
    return await base_repo_es_wrapper.cat_indices(index=klass)


async def does_index_exists(klass: str) -> bool:
    return await base_repo_es_wrapper.does_index_exists(index=klass)


async def create_index(klass: str, settings: Any, mappings: Any):
    return await base_repo_es_wrapper.create_index(
        index=klass, settings=settings, mappings=mappings
    )


async def delete_index(klass: str) -> Any:
    return await base_repo_es_wrapper.delete_index(index=klass)


async def get(klass: str, id: int) -> Any:
    return await base_repo_es_wrapper.get(index=klass, id=id)


async def get_all(klass: str) -> Any:
    return await base_repo_es_wrapper.get_all(index=klass)


async def get_latest(klass: str) -> Any:
    return await base_repo_es_wrapper.get_latest(index=klass)


async def update(index, id: int):
    return await base_repo_es_wrapper.update(index=index, id=id)


async def delete(klass: str, id: int) -> Any:
    return await base_repo_es_wrapper.delete(index=klass, id=id)
