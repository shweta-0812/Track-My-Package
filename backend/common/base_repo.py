import time
from typing import Any, Optional

from services import es_service as ESService


def get_current_timestamp():
    return int(time.time())


def generate_document_index_from_klass(klass: str) -> str:
    return f"{klass}"


async def create(klass: str, doc_data=Any, doc_version=1):
    index = generate_document_index_from_klass(klass=klass)
    doc = dict(
        **doc_data,
        doc_version=doc_version,
        created_at=get_current_timestamp(),
        updated_at=get_current_timestamp(),
    )
    return await ESService.ingest(index=index, doc=doc)


async def cat_indices(klass: Optional[str] = None):
    index = generate_document_index_from_klass(klass=klass)
    return await ESService.cat_indices(index=index)


async def does_index_exists(klass: str) -> bool:
    return await ESService.does_index_exists(index=klass)


async def create_index(klass: str, settings: Any, mappings: Any):
    index = generate_document_index_from_klass(klass=klass)
    return await ESService.create_index(
        index=index, settings=settings, mappings=mappings
    )


async def get(klass: str) -> Any:
    index = generate_document_index_from_klass(klass=klass)
    return await ESService.search(index=index, query={})

async def get_all(klass: str) -> Any:
    index = generate_document_index_from_klass(klass=klass)
    return await ESService.search(index=index, query={"sort": {"date": "desc"}, "query": {"match_all": {}}},)


async def get_latest(klass: str) -> Any:
    index = generate_document_index_from_klass(klass=klass)
    return await ESService.search(
        index=index,
        query={"size": 1, "sort": {"date": "desc"}, "query": {"match_all": {}}},
    )


async def update(klass, index, doc, doc_version):
    pass


async def delete(klass: str, id: str) -> Any:
    index = generate_document_index_from_klass(klass=klass)
    return await ESService.delete(
        index=index,
        id=id
    )

