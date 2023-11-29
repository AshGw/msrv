from typing import Dict

from fastapi import Body
from pydantic import BaseModel


class BaseContentResponse(Dict):
    pass


class EncodedImageResponse(BaseContentResponse):
    def __init__(self, *, encoded: bool, prompt: str, image: str) -> None:
        super().__init__(encoded=encoded, prompt=prompt, image=image)


class Prompt(BaseModel):
    prompt: str = Body(min_length=1, max_length=255)
