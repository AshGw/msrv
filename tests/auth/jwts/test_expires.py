from datetime import datetime, timedelta

import jwt

from msrv.security.auth.jwts import ALGORITHM, SECRET, jwt_decode, jwt_encode


def is_expired_token(
    encoded_token: str, secret: str = SECRET, algorithm: str = ALGORITHM
) -> bool:
    decoded_data = jwt_decode(
        encoded_token=encoded_token, secret=secret, algorithm=algorithm
    )
    return decoded_data is None


def test_jwt_encode_expired_token():
    expired_token = jwt_encode(email="excommunicado@gmail.com", scope={"client": "pro"})
    # Altering with the 'exp' field to make the token expired
    expired_payload = jwt.decode(expired_token, SECRET, algorithms=[ALGORITHM])
    expired_payload["exp"] = datetime.utcnow() - timedelta(days=1)
    modified_expired_token = jwt.encode(expired_payload, SECRET, algorithm=ALGORITHM)

    assert is_expired_token(encoded_token=modified_expired_token)
