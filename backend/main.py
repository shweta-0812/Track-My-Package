from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import AsyncElasticsearch

from api.v1.urls import api_v1_base_router

app = FastAPI()
app.include_router(api_v1_base_router, prefix='/api/v1')

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# homepage - to do
# @app.get("/")
# async def homepage(request):


# health check api
@app.get("/ping")
async def ping():
    return {"message": "pong"}

async_es_client = AsyncElasticsearch("http://localhost:9200")
@app.get("/test-es-cluster-health")
async def test_es_cluster_health():
    return await async_es_client.cluster.health()