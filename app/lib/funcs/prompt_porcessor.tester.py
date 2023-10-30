import uuid
from typing import Callable, List

from app.lib.hf.consts import Models, ReadAccessTokens
from app.lib.hf.switcher import get_valid_token
from app.lib.images.saver import ImageSaver
from app.lib.main import HFServiceCoordinator
from app.lib.parallelism.main import Executioner


class PromptProcessor:
    def __init__(
        self, *, output_folder: str, prompt: str, use_prompt_enhancers: bool = False
    ) -> None:
        self.used_cases = []
        self.output_folder = output_folder
        self.prompt = prompt
        self.use_prompt_enhancers = use_prompt_enhancers
        self.raw_image = b""

    def save_image(self) -> "PromptProcessor":
        ImageSaver(raw_bytes=self.raw_image).save(
            folder=self.output_folder, output_file_name=uuid.uuid4().hex
        )
        return self

    def run_HFSC(self) -> bytes:
        promptX = self.prompt
        print(promptX)
        x = HFServiceCoordinator(
            prompt=promptX,
            starter_hg_token=get_valid_token(),
            diffusion_model=Models.IMAGE,
            prompt_model=Models.PROMPT,
            use_prompt_enhancers=self.use_prompt_enhancers,
        )
        raw_image = x.get_raw_image()
        self.raw_image = raw_image
        self.save_image()  # TODO: NOT SAVE IT BUT RATHER OMIT THIS ONE
        return bytes(raw_image)

    def get_callables(self, num_funcs: int) -> List[Callable]:
        if num_funcs > 10 or num_funcs < 1:
            raise ValueError(
                "The number of passed functions should be between 1 and 10"
            )
        callables: List[Callable] = []
        for i in range(num_funcs):
            callables.append(self.run_HFSC)
        return callables


# Usage example:
if __name__ == "__main__":
    prompt = "scarlette johansson"
    # This is for quick testing of multiple executions at a time
    callables = PromptProcessor(
        output_folder="output", prompt=prompt, use_prompt_enhancers=False
    ).get_callables(10)

    Executioner.cores_limited_multiprocessor(callables, max_workers=10)
    # max cores are automatically set to the host's
