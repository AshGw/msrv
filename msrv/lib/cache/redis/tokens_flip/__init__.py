from msrv.lib.cache.redis.tokens_flip._redis import RedisSng
from msrv.lib.cache.redis.tokens_flip._redis import Redis
from msrv.lib.cache.redis.tokens_flip.config import RedisConf

r: Redis = RedisSng().use(local=RedisConf.use_local.value)


def initialize_tokens_cache() -> None:
    r.set(name="init", value="done")


# initialize_tokens_cache()
