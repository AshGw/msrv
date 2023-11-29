from msrv.lib.hf._diffuser import run_diffuser, HFDiffuserResponse
from msrv.lib.hf._prompter import run_prompter, HFPrompterResponse


class HFServiceCoordinator:
    generated_text: str
    generated_image: bytes

    def __init__(
        self,
        *,
        prompt: str,
        use_prompt_enhancers: bool = False,
    ) -> None:
        self.prompt = prompt
        self.use_prompt_enhancers = use_prompt_enhancers

    async def run_diffuser(self) -> HFDiffuserResponse:
        prompt = self.prompt
        if self.use_prompt_enhancers:
            _ = await self.run_prompter()
            prompt = _.generated_text
        res = await run_diffuser(prompt=prompt)
        return res

    async def run_prompter(self) -> HFPrompterResponse:
        res = await run_prompter(prompt=self.prompt)
        return res


if __name__ == "__main__":
    import asyncio

    async def _main(prompt: str):
        tasks = [HFServiceCoordinator(prompt=prompt).run_prompter() for _ in range(3)]
        await asyncio.gather(*tasks)

    asyncio.run(_main("astronaut"))
