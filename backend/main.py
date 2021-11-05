import time
from functools import lru_cache

import aioredis
from loguru import logger
from fastapi import FastAPI, Request, Response
from typing import Callable, Any
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import AsyncElasticsearch
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.templating import Jinja2Templates

from api.v1.urls import api_v1_base_router
from common.app_settings import app_settings

_loggers = {0}

def redis_init() -> Any:
    pool = aioredis.ConnectionPool.from_url("redis://localhost",
                                            max_connections=10)
    redis = aioredis.Redis(connection_pool=pool)

@lru_cache()
def settings_init() -> Any:
    return app_settings

def logger_init() -> None:
    global _loggers

    try:
        for handler_id in _loggers:
            logger.remove(handler_id)
    except Exception:
        pass

    handler_id = logger.add(
        sink=f"file_{time.time()}.log",
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        level="DEBUG",
        enqueue=True,
        backtrace=False,
        serialize=True,
    )

    _loggers.add(handler_id)
    logger.info("Initialized Loggers...")


def sentry_init() -> None:
    sentry_sdk.init(
        dsn="https://f640c637a07748fcaa38294a53707998@o1059451.ingest.sentry.io/6048078",
        traces_sample_rate=0.1,
        send_default_pii=True,
        environment="production" if app_settings.IS_PRODUCTION else "dev",
    )


async def sentry_exception(request: Request, call_next: Callable) -> Response:
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("request", request) # type: ignore
            sentry_sdk.capture_exception(e)
        raise e


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
