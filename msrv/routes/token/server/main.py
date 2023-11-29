import logging
from typing import Generator

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from msrv.lib.hf._parser import get_next_token, initialize_generator
from msrv.settings.urls import URL

route = APIRouter()


generator: Generator = initialize_generator()


@route.patch(URL.Token.Server.PREFIX, status_code=200, tags=["prod", "server"])
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
        logging.warning(e)
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
