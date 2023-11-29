from redis import Redis as Redis
from msrv.lib.cache.redis.tokens_flip._local_config import local_instance as li
from msrv.lib.cache.redis.tokens_flip._remote_config import remote_instance as ri


class RedisSng:
    """
    singleton, u can import it in other modules ( usually for testing )
    use this as a redis entrypoint.
    """

    _instance_remote: Redis = None
    _instance_local: Redis = None

    @classmethod
    def use(cls, local: bool = False) -> Redis:
        if local:
            if cls._instance_local is None:
                cls._instance_local = li
            return cls._instance_local
        else:
            if cls._instance_remote is None:
                cls._instance_remote = ri
            return cls._instance_remote
