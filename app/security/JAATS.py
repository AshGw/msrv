import os

import dotenv
import jwt

dotenv.load_dotenv()
SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"


def jwt_encode(
    *, email: str, scope: str, secret: str = SECRET, algorithm: str = ALGORITHM
) -> str:
    payload = {
        "email": email,
        "scope": scope,
    }
    jwt_token = jwt.encode(payload, secret, algorithm=algorithm)
    return jwt_token


def jwt_decode(*, encoded_token: str, secret: str = SECRET, algorithm: str = ALGORITHM):
    return jwt.decode(encoded_token, secret, algorithms=[algorithm])


user_email = "ashref.ag.me@gmail.com"
user_scope = "pro"
a = jwt_encode(email=user_email, scope=user_scope)
print(a)
b = jwt_decode(encoded_token=a)
print(b)
print(b.get("scope"))
