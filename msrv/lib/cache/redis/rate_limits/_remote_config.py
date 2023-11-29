import redis.asyncio as raio

from msrv.lib.env import Env


async def remote_instance():
    r = await raio.from_url(
        url=Env.Prod.Redis.RateLimitsCache.URL,
        encoding="utf-8",
        decode_responses=True,
    )
    return r
