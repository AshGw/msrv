from app.lib.hf.consts import Models
from app.lib.hf.switcher import get_valid_token
from app.lib.main import HFServiceCoordinator


class GenerateIMG:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.prompter = Models.PROMPT
        self.diffuser = Models.IMAGE

    def process(self, use_prompt_enhancers: bool = False) -> bytes:
        img = HFServiceCoordinator(
            prompt=self.prompt,
            starter_hg_token=get_valid_token(),
            diffusion_model=self.diffuser,
            prompt_model=self.prompter,
            use_prompt_enhancers=use_prompt_enhancers,
        ).get_raw_image()
        return bytes(img)
