from datetime import datetime, timedelta
from msrv.lib.env import Env
from typing import Any, Dict


SECRET: str = (
    Env.Dev.JWT_SECRET
    if Env.CURRENT_ENVIRONMENT == "development"
    else Env.Prod.JWT_SECRET
)

GOOGLE_ALGORITHM: str = "RS256"
ALGORITHM: str = "HS256"
EXPIRATION_PERIOD: int = 30  # days
IAT = datetime.utcnow()
EXP = IAT + timedelta(days=EXPIRATION_PERIOD)


def Payload(*, email: str, scope: Dict[str, Any], iat: datetime, exp: datetime):
    return {"email": email, "scope": scope, "iat": iat, "exp": exp}


def AnyPayload(
    *, payload: Dict[str, Any], scope: Dict[str, Any], iat: datetime, exp: datetime
):
    return {"payload": payload, "scope": scope, "iat": iat, "exp": exp}
