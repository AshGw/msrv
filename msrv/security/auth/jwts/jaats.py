from typing import Any, Dict
from jwt import encode, decode

from msrv.security.auth.jwts._definers import (
    Payload,
    AnyPayload,
    EXP,
    IAT,
    ALGORITHM,
    SECRET,
)


def jwt_encode(
    *, email: str, scope: dict, secret: str = SECRET, algorithm: str = ALGORITHM
) -> str:
    """
    :param email: Must be a valid gmail
    :param scope: Dictionary that holds either holds {"server":"sudo"} or {"client":"$PLAN"}
                  Plan can be either "free" || "hobby" || "pro"
    :param secret: This is automatically configured already to use .env's secret
    :param algorithm: HS256 by default, can be configured otherwise
    :return:
    """
    payload = Payload(email=email, scope=scope, iat=IAT, exp=EXP)
    jwt_token = encode(payload, secret, algorithm=algorithm)
    return jwt_token


def jwt_decode(
    *, encoded_token: str, secret: str = SECRET, algorithm: str = ALGORITHM
) -> dict | None:
    try:
        decoded_data = decode(encoded_token, secret, algorithms=[algorithm])
        return dict(decoded_data)
    except Exception:
        return None


def jwt_encode_any(
    *,
    payload: Dict[str, Any],
    scope: Dict[str, Any],
    secret: str = SECRET,
    algorithm: str = ALGORITHM
) -> str:
    """
    not available yet
    """
    payload = AnyPayload(payload=payload, scope=scope, iat=IAT, exp=EXP)
    jwt_token = encode(payload, secret, algorithm=algorithm)
    return jwt_token
