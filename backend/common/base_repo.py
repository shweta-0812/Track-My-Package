from typing import Any, Optional, Dict

import pydash

from common import base_repo_es_wrapper
from common.base_model import PTBaseModelStatusEnum

async def create(klass: str, doc_data=Any, doc_version=1):
    return await base_repo_es_wrapper.create(
        klass=klass, doc_data=doc_data, doc_version=doc_version
    )


async def cat_indices(klass: Optional[str] = None):
    return await base_repo_es_wrapper.cat_indices(klass=klass)


async def does_index_exists(klass: str) -> bool:
    return await base_repo_es_wrapper.does_index_exists(klass=klass)


async def create_index(klass: str, settings: Any, mappings: Any):
    return await base_repo_es_wrapper.create_index(
        klass=klass, settings=settings, mappings=mappings
    )


async def delete_index(klass: str) -> Any:
    return await base_repo_es_wrapper.delete_index(klass=klass)


async def get(klass: str, id: str) -> Any:
    result =  await base_repo_es_wrapper.get(klass=klass, id=id)
    if result:
        return pydash.head(result)

async def get_by_field(klass: str, field_name: str, field_value: str) -> Any:
    result = await base_repo_es_wrapper.get_by_field(klass=klass, field_value=field_value, field_name=field_name)
    if result:
        return pydash.head(result)


async def get_all(klass: str) -> Any:
    return await base_repo_es_wrapper.get_all(klass=klass)


async def get_lastest_doc(klass: str) -> Any:
    return await base_repo_es_wrapper.get_lastest_doc(klass=klass)


async def delete(klass: str, id: str, soft_delete: bool = True) -> Any:
    if not soft_delete:
        return await base_repo_es_wrapper.delete(klass=klass, id=id)
    return await update(
        klass=klass, id=id, status=PTBaseModelStatusEnum.IN_ACTIVE.value
    )


async def count(klass: str, filters: Dict[str, Any] = None) -> Any:
    return await base_repo_es_wrapper.count(klass=klass, filters=filters)


async def count_all(klass: str) -> Any:
    return await base_repo_es_wrapper.count_all(klass=klass)


async def _filter(klass: str, filters: Dict[str, Any] = None) -> Any:
    return await base_repo_es_wrapper._filter(klass=klass, filters=filters)


async def update(klass: str, id: str, **update_kwargs):
    return await base_repo_es_wrapper.update(klass=klass, id=id, **update_kwargs)
