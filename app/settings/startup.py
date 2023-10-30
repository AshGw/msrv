from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.lib.cache.rate_limits_cache import initialize_rate_limiter_cache
from app.lib.cache.tokens_cache_configs import initialize_tokens_cache


@asynccontextmanager
async def start_event(app: FastAPI):
    await initialize_rate_limiter_cache()
    initialize_tokens_cache()
    yield
