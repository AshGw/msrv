from typing import Optional
from hashlib import sha256
from base64 import urlsafe_b64encode
from secrets import token_urlsafe
from os import urandom


def create_code_challenge(code_verifier: str, method: Optional[str] = "S256") -> str:
    if method == "S256":
        hashed = sha256(code_verifier.encode()).digest()
        return urlsafe_b64encode(hashed).rstrip(b"=").decode()
    raise ValueError("Unsupported code challenge method")


BLOCK_SIZE: int = 16
code_verifier: str = token_urlsafe(BLOCK_SIZE)
print(create_code_challenge(code_verifier))
print(urlsafe_b64encode(sha256(urandom(16)).digest()).rstrip(b"=").decode())
