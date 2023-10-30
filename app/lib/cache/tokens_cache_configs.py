import os

import dotenv
from redis import Redis

dotenv.load_dotenv()

redis_tokens = Redis(
    host=os.getenv("TOKENS_REDIS_URL"),
    password=os.getenv("TOKENS_REDIS_PASSWORD"),
    port=int(os.getenv("TOKENS_REDIS_PORT")),
    ssl=True,
    decode_responses=True,
)


def initialize_tokens_cache():
    redis_tokens.set(name="init", value="done")
