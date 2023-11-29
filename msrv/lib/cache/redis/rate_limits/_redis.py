from redis.asyncio import Redis as AsyncRedis
from msrv.lib.cache.redis.rate_limits._local_config import local_instance as li
from msrv.lib.cache.redis.rate_limits._remote_config import remote_instance as ri


class AsyncRedisSng:
    """
    Async Redis singleton client.
    """

    _instance_remote: AsyncRedis = None
    _instance_local: AsyncRedis = None

    @classmethod
    async def use(cls, local: bool = False) -> AsyncRedis:
        if local:
            if cls._instance_local is None:
                cls._instance_local = await li()
            return cls._instance_local
        else:
            if cls._instance_remote is None:
                cls._instance_remote = await ri()
            return cls._instance_remote
