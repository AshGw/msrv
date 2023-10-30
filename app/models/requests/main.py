from fastapi import Body
from pydantic import BaseModel


class NextToken(BaseModel):
    next: bool


class PromptReq(BaseModel):
    prompt: str = Body(min_length=1, max_length=255)
