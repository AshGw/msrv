import pytest
from msrv.lib.cache.redis.rate_limits._redis import AsyncRedisSng, AsyncRedis


async def r() -> AsyncRedis:
    return await AsyncRedisSng.use(local=False)
    # turn to True when running inside a container if u needed to test the local redis server


@pytest.mark.asyncio
async def test_responds():
    _r = await r()
    await _r.ping()
