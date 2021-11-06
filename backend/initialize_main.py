import time
from functools import lru_cache
from typing import Any, Callable

import aioredis
import sentry_sdk
from loguru import logger
from starlette.requests import Request
from starlette.responses import Response

from common.app_settings import app_settings


_loggers = {0}


def redis_init() -> None:
    pool = aioredis.ConnectionPool.from_url(
        app_settings.REDIS_URL, max_connections=app_settings.REDIS_MAX_CONNECTIONS
    )
    aioredis.Redis(connection_pool=pool)


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
        sink=app_settings.LOGGER_SINK,
        rotation=app_settings.LOGGER_ROTATION_MEM_LIMIT,
        retention=app_settings.LOGGER_RETENTION_DAYS,
        level=app_settings.LOGGER_LOG_LEVEL,
        compression=app_settings.LOGGER_COMPRESSION,
        enqueue=app_settings.LOGGER_ENQUEUE,
        backtrace=app_settings.LOGGER_BACKTRACE,
        serialize=app_settings.LOGGER_SERIALIZE,
    )

    _loggers.add(handler_id)
    logger.info("Initialized Loggers...")


def sentry_init() -> None:
    sentry_sdk.init(
        dsn=app_settings.SENTRY_DSN,
        traces_sample_rate=app_settings.SENTRY_TRACES_SAMPLE_RATE,
        send_default_pii=True,
        environment="production" if app_settings.IS_PRODUCTION else "dev",
    )


async def sentry_exception(request: Request, call_next: Callable) -> Response:
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("request", request)  # type: ignore
            sentry_sdk.capture_exception(e)
        raise e
