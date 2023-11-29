from fastapi import APIRouter

from msrv.settings.urls import URL
from starlette.requests import Request

route = APIRouter()


@route.get(URL.Index.PREFIX, tags=["prod", "public"])
async def index(req: Request):
    a = req.headers.get("host")
    return {f"Hello is this the response i got {a} ": "mfs🔥"}
