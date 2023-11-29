import asyncio
import pytest
from typing import Annotated
from msrv.lib.hf._diffuser import run_diffuser

_NUMBER: Annotated[int, "Number of images to generate"] = 12


async def _main(prompt: str):
    tasks = [run_diffuser(prompt) for _ in range(_NUMBER)]
    await asyncio.gather(*tasks)


@pytest.mark.asyncio
async def test():  # no errors should occur
    await _main("van gogh painting")
