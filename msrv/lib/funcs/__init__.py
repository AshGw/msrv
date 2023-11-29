from datetime import datetime
import base64
from typing import Optional
from msrv.lib.hf.consts import Models
from msrv.lib.hf.coordinator import HFServiceCoordinator


class HFImageGen:
    def __init__(self, prompt: str) -> None:
        self.prompt = prompt
        self.prompter = Models.PROMPT
        self.diffuser = Models.IMAGE

    async def process(self, use_prompt_enhancers: bool = False) -> bytes:
        cls = HFServiceCoordinator(
            prompt=self.prompt,
            use_prompt_enhancers=use_prompt_enhancers,
        )
        img = await cls.run_diffuser()
        return img.generated_image


def serialize(raw: bytes, method: Optional[str] = "base64") -> str:
    if method == "base64":
        return base64.b64encode(raw).decode("utf-8")
    else:
        raise ValueError(f"Unsupported serialization method: {method}")


def current_time() -> str:
    return datetime.now().isoformat()
