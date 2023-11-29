import httpx

from msrv.lib.images.saver import ImageSaver
from msrv.lib.exceptions import Error200
from msrv.lib.hf._parser import get_random_token, parse_prompt
from msrv.lib.env import Env
from msrv.logger import logging
from msrv.lib.hf.consts import HFGetDiffuserAttrs
from msrv.lib.hf._interfaces import Endpoint, Header, Payload, HFDiffuserResponse
from uuid import uuid4


async def run_diffuser(prompt: str, save_image: bool = False) -> HFDiffuserResponse:
    _try_attempts: int = 0
    while True:
        logging.info(prompt)
        parsed = parse_prompt(prompt)
        payload = Payload(parsed_prompt=parsed)
        headers = Header(bearer_token=get_random_token())
        endpoint = Endpoint(model=Env.Prod.HF.DIFFUSER)
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=float(HFGetDiffuserAttrs.HTTPX_TIMEOUT),
                )
            if res.status_code == 200:
                raw_image = res.content
                if type(res.content) is bytes:
                    # TODO: IMAGE SAVING IS TO BE REMOVED
                    if save_image:
                        ImageSaver(raw_bytes=raw_image).save(
                            uuid4().hex,
                            folder=HFGetDiffuserAttrs.IMGSaver.OUTPUT_FOLDER,
                        )
                        logging.info("IMAGE SAVED")
                    logging.info("IMAGE GENERATED SUCCESSFULLY")
                    return HFDiffuserResponse(
                        generated_image=raw_image, loop_attempts=_try_attempts
                    )
                else:
                    _try_attempts += 1
                    logging.warning(
                        "STATUS IS 200 BUT THE IMAGE WAS NOT GENERATED"
                        f"Remaining Attempts: {HFGetDiffuserAttrs.MAX_TRY_ATTEMPTS - _try_attempts}"
                    )
                    if _try_attempts >= HFGetDiffuserAttrs.MAX_TRY_ATTEMPTS:
                        logging.fatal(
                            "Raising Error Due To Max Attempts Being Exhausted"
                        )
                        raise Error200()
            ...

        except Exception as e:
            if isinstance(e, httpx.ConnectError):
                _try_attempts += 1
                logging.error("Connection Error Just Hit", exc_info=True)
                if _try_attempts >= HFGetDiffuserAttrs.MAX_TRY_ATTEMPTS:
                    logging.fatal(
                        "Raising Error Due To Max Attempts Being Exhausted",
                        exc_info=True,
                    )
                    raise e
            else:
                logging.fatal("Raising Error: Unexpected Error Hit", exc_info=True)
                raise e
