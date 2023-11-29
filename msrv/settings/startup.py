from contextlib import asynccontextmanager

from fastapi import FastAPI

from msrv.lib.cache.redis.rate_limits import initialize_rate_limiter_cache
from msrv.lib.cache.redis.tokens_flip import initialize_tokens_cache


@asynccontextmanager
async def start_event(app: FastAPI):
    await initialize_rate_limiter_cache()
    initialize_tokens_cache()
    yield
