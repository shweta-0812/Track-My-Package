from typing import Any, Optional, Dict

from common import base_repo_es_wrapper
from common.base_model import PTBaseModelStatusEnum

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


async def get(klass: str, id: str) -> Any:
    return await base_repo_es_wrapper.get(index=klass, id=id)


async def get_all(klass: str) -> Any:
    return await base_repo_es_wrapper.get_all(index=klass)


async def get_latest(klass: str) -> Any:
    return await base_repo_es_wrapper.get_latest(index=klass)


async def delete(klass: str, id: str, soft_delete: bool = True) -> Any:
    if not soft_delete:
        return await base_repo_es_wrapper.delete(index=klass, id=id)
    return await update(
        klass=klass, id=id, status=PTBaseModelStatusEnum.IN_ACTIVE.value
    )


async def count(klass: str, filters: Dict[str, Any] = None) -> Any:
    return await base_repo_es_wrapper.count(index=klass, filters=filters)


async def count_all(klass: str) -> Any:
    return await base_repo_es_wrapper.count_all(index=klass)


async def _filter(klass: str, filters: Dict[str, Any] = None) -> Any:
    return await base_repo_es_wrapper._filter(index=klass, filters=filters)


async def update(klass: str, id: str, **update_kwargs):
    return await base_repo_es_wrapper.update(index=klass, id=id, **update_kwargs)
