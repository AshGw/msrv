import os
from typing import Dict

import dotenv

dotenv.load_dotenv()


class StringAttributes(type):
    def __new__(cls, name: str, bases: tuple, dct: Dict[str, str]):
        for key, value in dct.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise TypeError(f"All attributes of {name} must be strings.")
        return super().__new__(cls, name, bases, dct)


class URLS:
    HF = os.getenv("HF_URL")


class StatusCodes:
    RATE_LIMIT = 429
    LOADING = 503
    SUCCESS = 200


class Models(metaclass=StringAttributes):
    IMAGE = os.getenv("IMAGE_DIFFUSER_MODEL")
    PROMPT = os.getenv("PROMPT_DIFFUSER_MODEL")


class PersonalKeys(metaclass=StringAttributes):
    MY_API_KEY = os.getenv("PERSONAL_HF_API_KEY")
    MY_API_KEY2 = os.getenv("PERSONAL_HF_API_KEY2")


class ReadAccessTokens(metaclass=StringAttributes):
    FALLBACK_TOKEN_0 = os.getenv("FALLBACK_TOKEN_0")
    FALLBACK_TOKEN_1 = os.getenv("FALLBACK_TOKEN_1")
    FALLBACK_TOKEN_2 = os.getenv("FALLBACK_TOKEN_2")
    FALLBACK_TOKEN_3 = os.getenv("FALLBACK_TOKEN_3")
    FALLBACK_TOKEN_4 = os.getenv("FALLBACK_TOKEN_4")
    FALLBACK_TOKEN_5 = os.getenv("FALLBACK_TOKEN_5")
    FALLBACK_TOKEN_6 = os.getenv("FALLBACK_TOKEN_6")
    FALLBACK_TOKEN_7 = os.getenv("FALLBACK_TOKEN_7")
    FALLBACK_TOKEN_8 = os.getenv("FALLBACK_TOKEN_8")
    FALLBACK_TOKEN_9 = os.getenv("FALLBACK_TOKEN_9")
  
