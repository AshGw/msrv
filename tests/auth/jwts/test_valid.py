import pytest

from msrv.security.auth.jwts import ALGORITHM, SECRET, jwt_decode, jwt_encode

EMAIL: str = "valid@gmail.com"
CLIENT_SCOPE: dict = {"client": "pro"}


@pytest.fixture
def valid_token() -> str:
    return jwt_encode(email=EMAIL, scope=CLIENT_SCOPE)


def is_valid_token(
    encoded_token: str, secret: str = SECRET, algorithm: str = ALGORITHM
) -> bool:
    decoded_data = jwt_decode(
        encoded_token=encoded_token, secret=secret, algorithm=algorithm
    )
    return decoded_data is not None


def test_is_valid_token(valid_token):
    assert is_valid_token(encoded_token=valid_token)


def test_jwt_encode_and_decode(valid_token: str):
    decoded_token = jwt_decode(encoded_token=valid_token)
    assert decoded_token is not None
    assert decoded_token["email"] == EMAIL
    assert decoded_token["scope"] == CLIENT_SCOPE
