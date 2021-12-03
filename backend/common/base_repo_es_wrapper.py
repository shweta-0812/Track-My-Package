from typing import Any, Optional, Dict

import pydash

from common.es_data_parser import ESDataParser
from services import es_service as ESService


def generate_document_index_from_index(klass: str) -> str:
    return f"{klass}"


async def create(klass: str, doc_data=Any, doc_version=1):
    doc = dict(**doc_data, doc_version=doc_version,)
    return await ESService.ingest_doc(index=klass, doc=doc)


async def cat_indices(klass: Optional[str] = None):
    return await ESService.cat_indices(index=klass)


async def does_index_exists(klass: str) -> bool:
    return await ESService.does_index_exists(index=klass)


async def create_index(klass: str, settings: Any, mappings: Any):
    return await ESService.create_index(
        index=klass, settings=settings, mappings=mappings
    )


async def delete_index(klass: str) -> Any:
    return await ESService.delete_index(index=klass)


async def get_by_field(klass: str, field_name: str, field_value: str) -> Any:
    match = {}
    match[field_name] = {
        "query": field_value
      }
    body = {
        "query": {
    "match": match
  }
    }
    resp_data = await ESService.search_docs(index=klass, body=body)
    es_parsed_data = ESDataParser(resp_data)
    data = es_parsed_data.hits_data_details
    result = []

    def cb(elem):
        original_data = elem["_source"]
        original_data["id"] = elem["_id"]
        result.append(original_data)

    pydash.for_each(data, cb)
    return result


async def get(klass: str, id: str) -> Any:
    resp_data = await ESService.get_doc(index=klass, id=id)
    es_parsed_data = ESDataParser(resp_data)
    data = es_parsed_data.hits_data_details
    result = []

    def cb(elem):
        original_data = elem["_source"]
        original_data["id"] = elem["_id"]
        result.append(original_data)

    pydash.for_each(data, cb)
    return result


async def get_all(klass: str) -> Any:
    resp_data = await ESService.search_docs(
        index=klass, body={"sort": {"date": "desc"}, "query": {"match_all": {}}},
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


async def get_lastest_doc(klass: str) -> Any:
    resp_data = await ESService.search_docs(
        index=klass,
        body={"size": 1, "sort": {"date": "desc"}, "query": {"match_all": {}}},
    )
    es_parsed_data = ESDataParser(resp_data)
    data = es_parsed_data.hits_data_details
    if data:
        result = []
        def cb(elem):
            original_data = elem["_source"]
            original_data["id"] = elem["_id"]
            result.append(original_data)

        pydash.for_each(data, cb)
        return result
    return None


async def update(klass: str, id: str, **update_kwargs) -> Any:
    body={"query": {}}
    resp_data = await ESService.update_doc(index=klass, id=id, body=body)
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


async def _filter(klass: str, filters: Dict[str, Any] = None) -> Any:
    if filters is None:
        return None
    body = {"query": generate_filters_query(filters=filters)}
    resp_data = await ESService.search_docs(index=klass, body=body)
    return resp_data


async def count(klass: str, filters: Dict[str, Any] = None) -> Any:
    body = {"size": 0, "track_total_hits": True}
    if filters is not None:
        body["query"] = generate_filters_query(filters=filters)
    resp_data = await ESService.search_docs(index=klass, body=body)
    return resp_data


async def count_all(klass: str) -> Any:
    resp_data = await ESService.count_all_docs(index=klass)
    return resp_data


async def delete(klass: str, id: str) -> Any:
    index = generate_document_index_from_index(index=klass)
    return await ESService.delete_doc(index=klass, id=id)
