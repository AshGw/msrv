from typing import Final
from dataclasses import dataclass

from msrv.lib.env import Env, EnvStringAttributes


@dataclass
class HFGetAttrs:
    MAX_TRY_ATTEMPTS: Final[int] = 50
    HTTPX_TIMEOUT: Final[str | int] = "inf"
    HF_MIN_PROMPT_SIZE: Final[int] = 1
    HF_MAX_PROMPT_SIZE: Final[int] = 255


@dataclass
class HFSGetPrompterAttrs(HFGetAttrs):
    NUMBER = 40
    HF_SUCCESS_TEXT_GEN_RESPONSE: str = "generated_text"


@dataclass
class HFGetDiffuserAttrs(HFGetAttrs):
    class IMGSaver:
        OUTPUT_FOLDER: Final[str] = "output"


@dataclass
class URLS:
    HF = Env.Prod.HF.URL


@dataclass
class StatusCodes:
    RATE_LIMIT = 429
    LOADING = 503
    SUCCESS = 200


@dataclass
class Models:
    IMAGE = Env.Prod.HF.DIFFUSER
    PROMPT = Env.Prod.HF.PROMPTER


@dataclass
class PersonalKeys(metaclass=EnvStringAttributes):
    MY_API_KEY = Env.Prod.HF.KEYS.Personal.PERSONAL_HF_API_KEY
    MY_API_KEY2 = Env.Prod.HF.KEYS.Personal.PERSONAL_HF_API_KEY2
