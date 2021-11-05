from typing import Any, Optional

from elasticsearch import AsyncElasticsearch, ElasticsearchException
from elasticsearch._async.helpers import async_streaming_bulk

from common.app_settings import app_settings
from common.decorators import TFunc


def es_exception_handler(func: TFunc) -> TFunc:
    def inner(*args: str, **kwargs: dict) -> Any:
        try:
            retval = func(*args, **kwargs)
            return retval
        except Exception as e:
            print("::::::::::::;my exception:::::::")
            print(e)

    return inner


async_es_client = AsyncElasticsearch(app_settings.ES_DATABASE_URL)


@es_exception_handler
async def ingest(index: str, doc: Any) -> Any:
    if not (await async_es_client.indices.exists(index=index)):
        body = {"settings": {}, "mappings": {}}
        await async_es_client.indices.create(index=index, body=body)
    doc_type = None
    doc_id = doc.pop("id")
    await async_es_client.index(index=index, document=doc, doc_type=doc_type, id=doc_id)


@es_exception_handler
async def does_index_exists(index: str) -> bool:
    try:
        return await async_es_client.indices.exists(index=index)
    except Exception as e:
        print(e)
        return False

@es_exception_handler
async def create_index(index: str, settings: Any, mappings: Any) -> Any:
    if not (await async_es_client.indices.exists(index=index)):
        body = {"settings": settings, "mappings": mappings}
        await async_es_client.indices.create(index=index, body=body)
    return None

async def delete_index(index: str) -> Any:
    if await async_es_client.indices.exists(index=index):
        await async_es_client.indices.delete(index=index)
    return None


@es_exception_handler
async def cat_indices(index: Optional[str] = None) -> Any:
    return await async_es_client.cat.indices()


@es_exception_handler
async def cat_indices_target(index: Optional[str] = None) -> Any:
    return await async_es_client.cat.indices(index=index)




async def get(index: str, id: int) -> Any:
    try:
        return await async_es_client.get(index=index, id=id)
    except ElasticsearchException as e:
        if type(e).__name__ == "NotFoundError":
            return None
        
async def search(index: str, query: Any) -> Any:
    try:
        return await async_es_client.search(index=index, body=query)
    except ElasticsearchException as e:
        if type(e).__name__ == "NotFoundError":
            return None

async def delete(index: str, id: str ) -> Any:
    try:
        return await async_es_client.delete(index=index, id=id)
    except ElasticsearchException as e:
        if type(e).__name__ == "NotFoundError":
            return None

# async def bulk_ingest( index, docs):
#     async for _ in async_streaming_bulk(
#         client=async_es_client, index=index, actions=None
#     ):
#         pass
#     return {"status": "ok"}
# async def delete( index):
#     return await async_es_client.delete_by_query(index=index, body={"query": {"match_all": {}}})
#
#
# async def delete_id(id):
#     try:
#         return await es.delete(index="games", id=id)
#     except NotFoundError as e:
#         return e.info, 404
#
#
# async def update(self):
#     response = []
#     docs = await es.search(
#         index="games", body={"query": {"multi_match": {"query": ""}}}
#     )
#     now = datetime.datetime.utcnow()
#     for doc in docs["hits"]["hits"]:
#         response.append(
#             await es.update(
#                 index="games", id=doc["_id"], body={"doc": {"modified": now}}
#             )
#         )
#
#     return jsonable_encoder(response)
#
#
# async def error(self):
#     try:
#         await es.delete(index="games", id="somerandomid")
#     except NotFoundError as e:
#         return e.info
#
#
# async def get_doc(id):
#     return await es.get(index="games", id=id)
