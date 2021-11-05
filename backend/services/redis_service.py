from typing import AsyncIterator

from aioredis import create_redis_pool, Redis

from common.app_settings import app_settings


async def init_redis_pool(host: str = app_settings.REDIS_URL) -> AsyncIterator[Redis]:
    pool = await create_redis_pool(f"redis://{host}")
    yield pool
    pool.close()
    await pool.wait_closed()