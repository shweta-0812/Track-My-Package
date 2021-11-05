import pydash
from typing import Any, Optional
from loguru import logger
from services import es_service as ESService
from common.es_data_parser import ESDataParser


def generate_document_index_from_index(index: str) -> str:
    return f"{index}"


async def create(index: str, doc_data=Any, doc_version=1):
    index = generate_document_index_from_index(index=index)
    doc = dict(**doc_data, doc_version=doc_version,)
    return await ESService.ingest(index=index, doc=doc)


async def cat_indices(index: Optional[str] = None):
    index = generate_document_index_from_index(index=index)
    return await ESService.cat_indices(index=index)


async def does_index_exists(index: str) -> bool:
    return await ESService.does_index_exists(index=index)


async def create_index(index: str, settings: Any, mappings: Any):
    index = generate_document_index_from_index(index=index)
    return await ESService.create_index(
        index=index, settings=settings, mappings=mappings
    )


async def delete_index(index: str) -> Any:
    index = generate_document_index_from_index(index=index)
    return await ESService.delete_index(index=index)


async def get(index: str, id: int) -> Any:
    index = generate_document_index_from_index(index=index)
    resp_data = await ESService.get(index=index, id=id)
    es_parsed_data = ESDataParser(resp_data)
    data = es_parsed_data.hits_data_details
    result = []

    def cb(elem):
        original_data = elem["_source"]
        original_data["id"] = elem["_id"]
        result.append(original_data)

    pydash.for_each(data, cb)
    return result


async def get_all(index: str) -> Any:
    index = generate_document_index_from_index(index=index)
    resp_data = await ESService.search(
        index=index, query={"sort": {"date": "desc"}, "query": {"match_all": {}}},
    )
    es_parsed_data = ESDataParser(resp_data)
    data = es_parsed_data.hits_data_details
    result = []

    def cb(elem):
        original_data = elem["_source"]
        original_data["id"] = elem["_id"]
        result.append(original_data)

    pydash.for_each(data, cb)
    return result


async def get_latest(index: str) -> Any:
    index = generate_document_index_from_index(index=index)
    resp_data = await ESService.search(
        index=index,
        query={"size": 1, "sort": {"date": "desc"}, "query": {"match_all": {}}},
    )
    es_parsed_data = ESDataParser(resp_data)
    data = es_parsed_data.hits_data_details
    result = []

    def cb(elem):
        original_data = elem["_source"]
        original_data["id"] = elem["_id"]
        result.append(original_data)

    pydash.for_each(data, cb)
    return result

async def update(index: str, id: int) -> Any:
    pass


async def delete(index: str, id: int) -> Any:
    index = generate_document_index_from_index(index=index)
    return await ESService.delete(index=index, id=id)
