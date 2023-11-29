from typing import List
from itertools import chain
from msrv.lib.env import Env

_allowed_prod_origins: List[str] = Env.Prod.Origins.ALL_ORIGINS_LIST
_allowed_dev_origins: List[str] = Env.Dev.Origins.ALL_ORIGINS_LIST

origins = list(chain(_allowed_prod_origins, _allowed_dev_origins))

options = {
    "headers": ["Authorization"],
    "methods": ["GET", "POST", "OPTIONS"],
    "origins": origins,
    "credentials": True,
}
