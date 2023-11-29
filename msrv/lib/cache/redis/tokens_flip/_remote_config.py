from redis import Redis
from msrv.lib.env import Env

remote_instance: Redis = Redis(
    host=Env.Prod.Redis.TokensCache.URL,
    password=Env.Prod.Redis.TokensCache.PASSWORD,
    port=Env.Prod.Redis.TokensCache.PORT,
    ssl=True,
    decode_responses=True,
)
