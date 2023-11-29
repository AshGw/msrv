import asyncio
import pytest

from typing import Annotated
from msrv.lib.hf._prompter import run_prompter


_NUMBER: Annotated[int, "Number of prompts to generate"] = 12


async def _main(prompt: str):
    tasks = [run_prompter(prompt) for _ in range(_NUMBER)]
    await asyncio.gather(*tasks)


@pytest.mark.asyncio
async def test():  # no errors should occur
    await _main("van gogh painting")
