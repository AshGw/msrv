from msrv.lib.cache.redis.tokens_flip._redis import RedisSng, Redis

r: Redis = RedisSng.use(local=False)
# turn to True when running inside a container if u needed to test the local redis server


def test_redis_connection():
    assert r.ping() is True
