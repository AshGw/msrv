from typing import Annotated, Generator

from fastapi import HTTPException, Query, Request
from starlette.responses import JSONResponse, Response

from app.lib.funcs.gen import GenerateIMG
from app.lib.funcs.serializer import serialize
from app.lib.hf.parser import get_next_token, initialize_generator
from app.lib.logger.main import current_time, logging_service
from app.models.requests.main import PromptReq
from app.settings.configs import ASCM
from app.settings.consts import Route

apx = (
    ASCM().enable(oauth2=True, cors=True, overload_watch=True, rate_limits=True).build()
)


@apx.post(Route.SERVER_GENERATE, tags=["prod", "server"])
async def send_image(
    prompt: PromptReq,
    encode: Annotated[bool, Query()] = False,
):
    res = {}
    try:
        image_bytes = GenerateIMG(prompt=prompt.prompt).process()
        if encode:
            res.update(
                encoded=encode, prompt=prompt.prompt, image=serialize(image_bytes)
            )
            return JSONResponse(content=res, status_code=200)

        return Response(content=image_bytes, media_type="image/jpeg", status_code=200)
    except Exception as e:
        logging_service(message=str(e), time=current_time())
        return JSONResponse(
            {"error": "The 3rd party service is currently unavailable"}, status_code=503
        )


@apx.options(Route.CLIENT_GENERATE, tags=["prod", "client"])
def allow_gen():
    return {"working": "good"}


@apx.post(Route.CLIENT_GENERATE, tags=["prod", "client"])
async def send_image(
    prompt: PromptReq,
    encode: Annotated[bool, Query()] = False,
    enhance: Annotated[bool, Query()] = False,
):

    use_prompt_enhancers: bool = enhance
    res = {}
    try:
        image_bytes = GenerateIMG(prompt=prompt.prompt).process(
            use_prompt_enhancers=use_prompt_enhancers
        )
        if encode:
            res.update(
                encoded=encode, prompt=prompt.prompt, image=serialize(image_bytes)
            )
            return JSONResponse(content=res, status_code=200)

        return Response(content=image_bytes, media_type="image/jpeg", status_code=200)
    except Exception as e:
        logging_service(message=str(e), time=current_time())
        return JSONResponse(
            {"error": "The 3rd party service is currently unavailable"}, status_code=503
        )


generator: Generator = initialize_generator()


@apx.patch(Route.SERVER_TOKEN_GENERATE, status_code=200, tags=["prod", "server"])
async def get_token(request: Request):
    """
    Get the next token based on the provided flag.

    If the 'next' flag is True, get the next token.
    If the 'next' flag is False, keep the same current working token.

    :param request: The FastAPI Request object.
    :param json_body: The request JSON object.
    - `next` (bool): If true, get the next token; if false, keep the same current working token.

    :return: The next token or an error message.
    :rtype: Dict[str, str]

    :example:
    - Request Body:
        ```json
            {"next": true}
        ```

    - Response:
        ```json
            {"token": "your_next_token_here"}

        ```
    """
    try:
        json_body = await request.json()
    except Exception as e:
        logging_service(message=str(e), time=current_time())
        return JSONResponse(content={"error": "Invalid JSON"}, status_code=422)
    while True:
        flag = json_body.get("next")
        if isinstance(flag, bool):
            return JSONResponse(
                content=get_next_token(generator=generator, flag=flag), status_code=200
            )
        return JSONResponse(
            content={"error": "next flag should be a boolean"}, status_code=406
        )


@apx.get("/", tags=["prod", "public"])
async def index():
    return {"Hello": "mfs🔥"}


@apx.exception_handler(404)
async def not_found(request: Request, exception: HTTPException):
    return JSONResponse(status_code=404, content={"404": "Not found"})
