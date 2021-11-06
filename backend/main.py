from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import AsyncElasticsearch
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.templating import Jinja2Templates

from api.v1.urls import api_v1_base_router
from common.app_settings import app_settings
from initialize_main import redis_init, settings_init, logger_init, sentry_init, \
    sentry_exception

app = FastAPI()
sentry_init()
app = SentryAsgiMiddleware(app).app
app.include_router(api_v1_base_router, prefix="/api/v1")

settings_init()

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=sentry_exception)

logger_init()
redis_init()

@app.get("/")
async def homepage(request: Request) -> Response:
    index_template = Jinja2Templates(directory="../static")
    return index_template.TemplateResponse("index.html", {"request": request})

# health check api
@app.get("/ping")
async def ping():
    return {"message": "pong"}


async_es_client = AsyncElasticsearch("http://localhost:9200")


@app.get("/test-es-cluster-health")
async def test_es_cluster_health():
    return await async_es_client.cluster.health()
