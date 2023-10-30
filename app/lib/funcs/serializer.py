import base64
from typing import Optional


def serialize(raw: bytes, method: Optional[str] = "base64") -> str | None:
    if method == "base64":
        return base64.b64encode(raw).decode("utf-8")
    pass  # TODO: will add methods later
