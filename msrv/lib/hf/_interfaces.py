from typing import Dict, Any
from msrv.lib.env import Env

# TODO: TEST THIS TOO G


class HFResponse(Dict):
    def __init__(self, *, loop_attempts: int = 0):
        self.loop_attempts = loop_attempts
        super().__init__(
            loop_attempts=self.loop_attempts,
        )


class HFPrompterResponse(HFResponse):
    def __init__(self, *, generated_text: str, **kwargs: Any):
        self.generated_text = generated_text
        super().__init__(**kwargs)


class HFDiffuserResponse(HFResponse):
    def __init__(self, *, generated_image: bytes, **kwargs: Any):
        self.generated_image = generated_image
        super().__init__(**kwargs)


def Header(*, bearer_token: str, **kwargs: Any) -> Dict[str, str]:
    return {"Authorization": f"Bearer {bearer_token}"}


def Payload(*, parsed_prompt: str, **kwargs: Any) -> Dict[str, str]:
    return {"inputs": parsed_prompt}


def Endpoint(*, endpoint: str = Env.Prod.HF.URL, model: str, **kwargs: Any) -> str:
    return f"{endpoint}/{model}"


class NextToken(Dict):
    def __init__(self, *, token_identifier: str, token: str, is_new: bool):
        self.token_identifier = token_identifier
        self.token = token
        self.is_new = is_new
        super().__init__(
            token_identifier=self.token_identifier, token=self.token, is_new=self.is_new
        )
