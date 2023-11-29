from redis.asyncio.client import Redis as AyncRedis
from fastapi_limiter import FastAPILimiter
from msrv.lib.cache.redis.rate_limits._redis import AsyncRedisSng
from msrv.lib.cache.redis.rate_limits.config import RedisConf


async def r() -> AyncRedis:
    """
    Use this instance as a singleton redis instance through the whole msrv.
    :return: async Redis client.
    """
    return await AsyncRedisSng().use(local=RedisConf.use_local.value)


async def initialize_rate_limiter_cache():
    return await FastAPILimiter.init(await r())
