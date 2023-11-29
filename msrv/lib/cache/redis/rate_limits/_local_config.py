import redis.asyncio as raio

from msrv.lib.env import Env

# TODO: COORDINATE WITH THE DOCKERIZATION PROCESS & SET THE ACTUAL PASSWORD G!


async def local_instance():
    r = await raio.from_url(
        url=Env.Prod.Redis.RateLimitsCacheLocal.URL,
        encoding="utf-8",
        decode_responses=True,
    )
    return r


async def local_instance_trial():
    await raio.client.Redis(
        host=Env.Prod.Redis.TokensCacheLocal.URL,
        port=int(Env.Prod.Redis.TokensCacheLocal.PORT),
        decode_responses=True,
        password=Env.Prod.Redis.TokensCacheLocal.PASSWORD,
    )
