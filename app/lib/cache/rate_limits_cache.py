import os

import dotenv
import redis.asyncio as raio
from fastapi_limiter import FastAPILimiter

dotenv.load_dotenv()


async def initialize_rate_limiter_cache():
    r = raio.from_url(
        url=os.getenv("RATE_LIMIT_REDIS_URL"),
        encoding="utf-8",
        decode_responses=True,
    )
    return await FastAPILimiter.init(r)
