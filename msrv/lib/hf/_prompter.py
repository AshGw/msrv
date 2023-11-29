import httpx

from msrv.lib.hf._parser import parse_prompt
from msrv.lib.exceptions import Error200
from msrv.lib.hf._parser import get_random_token
from msrv.lib.env import Env
from msrv.logger import logging
from msrv.lib.hf.consts import HFSGetPrompterAttrs
from msrv.lib.hf._interfaces import Endpoint, Header, Payload, HFPrompterResponse
from json import JSONDecodeError


async def run_prompter(prompt: str) -> HFPrompterResponse:
    _try_attempts: int = 0
    while True:
        parsed = parse_prompt(prompt)
        logging.info(prompt)
        payload = Payload(parsed_prompt=parsed)
        headers = Header(bearer_token=get_random_token())
        endpoint = Endpoint(model=Env.Prod.HF.PROMPTER)
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=float(
                        HFSGetPrompterAttrs.HTTPX_TIMEOUT
                    ),  # WARNING: INFINITE TIMEOUT
                )
            if res.status_code == 200:
                generated_text = res.json()[0].get(
                    HFSGetPrompterAttrs.HF_SUCCESS_TEXT_GEN_RESPONSE
                )
                if generated_text:
                    logging.info(generated_text)
                    return HFPrompterResponse(
                        generated_text=generated_text, loop_attempts=_try_attempts
                    )
                else:
                    _try_attempts += 1
                    logging.warning(
                        "STATUS IS 200 BUT THE TEXT WAS NOT GENERATED"
                        f"Remaining Attempts: {HFSGetPrompterAttrs.MAX_TRY_ATTEMPTS - _try_attempts}"
                    )
                    if _try_attempts >= HFSGetPrompterAttrs.MAX_TRY_ATTEMPTS:
                        logging.fatal(
                            "Raising Error Due To Max Attempts Being Exhausted"
                        )
                        raise Error200()
            ...
        except Exception as e:
            _try_attempts += 1
            if isinstance(e, httpx.ConnectError):
                logging.error("httpx.ConnectError Just Hit", exc_info=True)
                if _try_attempts >= HFSGetPrompterAttrs.MAX_TRY_ATTEMPTS:
                    logging.fatal(
                        "Raising Error Due To Max Attempts Being Exhausted",
                        exc_info=True,
                    )
                    raise e
            elif isinstance(e, JSONDecodeError):
                logging.error("JSONDecodeError Just Hit", exc_info=True)
                if _try_attempts >= HFSGetPrompterAttrs.MAX_TRY_ATTEMPTS:
                    logging.fatal(
                        "Raising Error Due To Max Attempts Being Exhausted",
                        exc_info=True,
                    )
                    raise e
            else:
                logging.fatal("Raising Error: Unexpected Error Hit", exc_info=True)
                raise e
