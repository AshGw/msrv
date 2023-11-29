from redis import Redis
from msrv.lib.env import Env

# TODO: COORDINATE WITH THE DOCKERIZATION PROCESS & SET THE ACTUAL PASSWORD G!


local_instance: Redis = Redis(
    host=Env.Prod.Redis.TokensCacheLocal.URL,
    port=int(Env.Prod.Redis.TokensCacheLocal.PORT),
    decode_responses=True,
    password=Env.Prod.Redis.TokensCacheLocal.PASSWORD,
)
