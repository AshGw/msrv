from typing import Annotated

from fastapi import APIRouter, Query
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, Response

from msrv.lib.funcs import HFImageGen, serialize
from msrv.logger import logging
from msrv.models import Prompt, EncodedImageResponse
from msrv.settings.urls import URL

PATH: str = URL.Generate.Free.PREFIX
route = APIRouter()


@route.options(PATH, tags=["prod", "client"])
def allow_gen():
    return JSONResponse(content="positive")


@route.post(PATH, tags=["prod", "client"])
async def send_image(
    prompt: Prompt,
    encode: Annotated[bool, Query()] = False,
    enhance: Annotated[bool, Query()] = False,
) -> Response:
    use_prompt_enhancers: bool = enhance
    try:
        logging.info(prompt.prompt)  # TODO: REMOVE IT
        image_bytes = await HFImageGen(prompt=prompt.prompt).process(
            use_prompt_enhancers=use_prompt_enhancers
        )
        if encode:
            return JSONResponse(
                content=EncodedImageResponse(
                    encoded=encode, prompt=prompt.prompt, image=serialize(image_bytes)
                ),
                status_code=200,
            )

        return Response(content=image_bytes, media_type="image/jpeg", status_code=200)
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(
            detail="one of our 3rd party services is currently unavailable",
            status_code=503,
        )
