from typing import List

from redis import Redis

from app.lib.cache.tokens_cache_configs import redis_tokens
from app.lib.hf.consts import ReadAccessTokens, StringAttributes
from app.lib.hf.parser import StringAttributeParser


class TokenAcquisition:
    def __init__(self, str_attrs_cls: StringAttributes, redis: Redis):
        self.str_attrs = StringAttributeParser(str_attrs_cls)
        self.r = redis

    def available_token(self):
        keys_dict: dict = self.str_attrs.turn_dict()
        limited_keys: list = redis_tokens.keys()
        available_key: str = ReadAccessTokens.FALLBACK_TOKEN_0
        for key in keys_dict.keys():
            if key in limited_keys:
                continue
            available_key = key
            break
        return available_key, keys_dict[available_key]


def set_limited_key(*, key: str, expiration: int = 3650):
    redis_tokens.setex(name=key, time=expiration, value="rate limited")


def get_limited_keys() -> List:
    return redis_tokens.keys()


def get_valid_token() -> str:
    available_key, token = TokenAcquisition(
        str_attrs_cls=ReadAccessTokens, redis=redis_tokens
    ).available_token()
    return token
