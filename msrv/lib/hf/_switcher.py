from typing import List, Tuple

from redis import Redis

from msrv.lib.cache.redis.tokens_flip import r as redis
from msrv.lib.env import Env, EnvStringAttributes
from msrv.lib.hf._parser import StringAttributeParser

_TOKENS_CLS = Env.Prod.HF.KEYS.ExecTokens


class TokenAcquisition:
    def __init__(self, str_attrs_cls: EnvStringAttributes, redis: Redis) -> None:
        self.str_attrs = StringAttributeParser(str_attrs_cls)
        self.r = redis

    def available_token(self) -> Tuple[str, str]:
        keys_dict: dict = self.str_attrs.turn_dict()
        limited_keys: list = redis.keys()
        available_key: str = _TOKENS_CLS.FALLBACK_TOKEN_0
        for key in keys_dict.keys():
            if key in limited_keys:
                continue
            available_key = key
            break
        return available_key, keys_dict[available_key]


def set_limited_key(*, key: str, expiration: int = 3650) -> None:  # in seconds
    redis.setex(name=key, time=expiration, value="rate limited")


def get_limited_keys() -> List[str | None]:
    return redis.keys()


def get_valid_token() -> str:
    _, token = TokenAcquisition(
        str_attrs_cls=_TOKENS_CLS, redis=redis
    ).available_token()
    return token
