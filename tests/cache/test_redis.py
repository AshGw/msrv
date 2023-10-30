import os

import dotenv
from redis import Redis

dotenv.load_dotenv()


def connect():
    return Redis(
        host=os.getenv("TOKENS_REDIS_URL"),
        password=os.getenv("TOKENS_REDIS_PASSWORD"),
        port=int(os.getenv("TOKENS_REDIS_PORT")),
        ssl=True,
        decode_responses=True,
    )


def test_redis_connection():
    r = connect()
    assert r.ping() is True


def test_init_value():
    r = connect()
    assert r.get("init") == "done"
