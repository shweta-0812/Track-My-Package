from typing import Any, Optional, Dict

import pydash

from common.es_data_parser import ESDataParser
from services import es_service as ESService


def generate_document_index_from_index(index: str) -> str:
    return f"{index}"


async def create(index: str, doc_data=Any, doc_version=1):
    index = generate_document_index_from_index(index=index)
    doc = dict(**doc_data, doc_version=doc_version,)
    return await ESService.ingest_doc(index=index, doc=doc)


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


async def get(index: str, id: str) -> Any:
    resp_data = await ESService.get_doc(index=index, id=id)
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
    resp_data = await ESService.search_docs(
        index=index, body={"sort": {"date": "desc"}, "query": {"match_all": {}}},
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
    resp_data = await ESService.search_docs(
        index=index,
        body={"size": 1, "sort": {"date": "desc"}, "query": {"match_all": {}}},
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


async def update(index: str, id: str, **update_kwargs) -> Any:
    print(update_kwargs)
    body={"query": {}}
    resp_data = await ESService.update_doc(index=index, id=id, body=body)
    return resp_data


def generate_filters_query(filters: Dict[str, Any] = None) -> Dict[str, Any]:
    # use filters to generate query
    # refer : https://towardsdatascience.com/deep-dive-into-querying-elasticsearch-filter-vs-query-full-text-search-b861b06bd4c0
    # refer : https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html

    query = {"constant_score": {"filter": []}}
    for key, value in filters.items():
        term = {"term": {}}
        term["term"][key] = value
        query["constant_score"]["filter"].append(term)
    return query


async def _filter(index: str, filters: Dict[str, Any] = None) -> Any:
    if filters is None:
        return None
    body = {"query": generate_filters_query(filters=filters)}
    resp_data = await ESService.search_docs(index=index, body=body)
    return resp_data


async def count(index: str, filters: Dict[str, Any] = None) -> Any:
    body = {"size": 0, "track_total_hits": True}
    if filters is not None:
        body["query"] = generate_filters_query(filters=filters)
    resp_data = await ESService.search_docs(index=index, body=body)
    return resp_data


async def count_all(index: str) -> Any:
    resp_data = await ESService.count_all_docs(index=index)
    return resp_data


async def delete(index: str, id: str) -> Any:
    index = generate_document_index_from_index(index=index)
    return await ESService.delete_doc(index=index, id=id)
