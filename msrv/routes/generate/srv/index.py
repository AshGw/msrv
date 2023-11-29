from typing import Annotated

from fastapi import APIRouter, Query
from starlette.responses import JSONResponse, Response
from starlette.exceptions import HTTPException

from msrv.lib.funcs import HFImageGen, serialize
from msrv.logger import logging
from msrv.models import Prompt, EncodedImageResponse
from msrv.settings.urls import URL

route = APIRouter()


@route.post(URL.Generate.Server.PREFIX, tags=["prod", "server"])
async def send_image(
    prompt: Prompt,
    encode: Annotated[bool, Query()] = False,
    enhance: Annotated[bool, Query()] = False,
) -> Response:
    use_prompt_enhancers: bool = enhance
    try:
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
