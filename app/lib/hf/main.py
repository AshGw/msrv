from typing import Any, Dict, Optional, Type, TypeVar

import requests

from app.lib.exceptions import EmptyPromptError
from app.lib.hf.consts import URLS

T = TypeVar("T")


class ResponseInfo:
    def __init__(
        self,
        content_type: Type[Any],
        content: Any,
        text: str,
        apparent_encoding: Type[Any],
        encoding: Type[Any],
        cookies: Type[Any],
        ok: bool,
        status_code: int,
        next: Optional[T] = None,
    ):
        self.content_type = content_type
        self.content = content
        self.text = text
        self.apparent_encoding = apparent_encoding
        self.encoding = encoding
        self.cookies = cookies
        self.ok = ok
        self.status_code = status_code
        self.next = next


class HF:
    response: requests.Response
    estimated_time: float = 0.0
    is_loading: bool = False
    is_overloaded: bool = False
    is_unknown: bool = False
    reached_rate_limit: bool = False
    is_token_invalid: bool = False
    is_unseen_error: bool = False

    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def send(self, prompt: str) -> "HF":
        if len(prompt) < 1:
            raise EmptyPromptError()
        # TODO: MUST CHECK IN THE API ENDPOINT THAT THE PROMPT SHALL NEVER BE EMPTY
        payload = {"inputs": prompt}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        endpoint = f"{URLS.HF}/{self.model}"
        self.response = requests.post(endpoint, headers=headers, json=payload)
        res = self.response

        try:
            approx = res.json()["estimated_time"]
            if approx:
                self.is_loading = True
                self.estimated_time = approx

        except (ValueError, TypeError, KeyError):
            pass
        try:
            if res.json()["error"] == "overloaded":
                self.is_overloaded = True

        except (ValueError, TypeError, KeyError):
            pass

        try:
            if res.json()["error"] == "unknown error":
                self.is_unknown = True

        except (ValueError, TypeError, KeyError):
            pass

        try:
            if res.status_code == 429:
                self.reached_rate_limit = True

        except (ValueError, TypeError, KeyError):
            pass

        try:
            if (
                res.json()["error"]
                == "Authorization header is correct, but the token seems invalid"
            ):
                self.is_token_invalid = True

        except (ValueError, TypeError, KeyError):
            pass
        try:
            if (
                res.json()["error"]
                and not self.is_token_invalid
                and not self.reached_rate_limit
                and not self.is_overloaded
            ):
                self.is_unseen_error = True

        except (ValueError, TypeError, KeyError):
            pass

        return self

    @property
    def result(self) -> ResponseInfo:
        res = self.response
        return ResponseInfo(
            content_type=type(res.content),
            content=res.content,
            text=res.text,
            apparent_encoding=type(res.apparent_encoding),
            encoding=type(res.encoding),
            cookies=type(res.cookies),
            ok=res.ok,
            status_code=res.status_code,
            next=res.next,
        )

    def json(self) -> requests.Response:
        return self.response.json()

    def safe_json(self) -> requests.Response | None:
        try:
            return self.response.json()
        except requests.exceptions.JSONDecodeError:
            return None

    def get_attrs(self) -> Dict[str, bool | float]:
        return {
            "status_code": self.response.status_code,
            "estimated_time": self.estimated_time,
            "is_token_invalid": self.is_token_invalid,
            "is_loading": self.is_loading,
            "is_overloaded": self.is_overloaded,
            "is_error_unknown": self.is_unknown,
            "is_unseen_error": self.is_unseen_error,
            "reached_rate_limit": self.reached_rate_limit,
        }

    def error(self) -> str | None:
        try:
            return str(self.response.json()[0]["error"])
        except (ValueError, TypeError, KeyError, IndexError):
            return

    def generated_text(self) -> str | None:
        try:
            return str(self.response.json()[0]["generated_text"])
        except (ValueError, TypeError, KeyError, IndexError):
            return

    def safe_bytes_content(self):
        try:
            return self.result.content
        except (ValueError, TypeError, KeyError, IndexError):
            return None

    def generated_raw_image(self) -> bytes | None:
        return self.safe_bytes_content()
