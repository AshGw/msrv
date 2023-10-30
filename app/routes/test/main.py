from fastapi import APIRouter

from app.settings.consts import TestRoute

route = APIRouter()


@route.get(TestRoute.CLIENT_RATE_LIMITER, tags=["test"])
async def fn1():
    return {"Homie almost yeeted out": "😥"}


@route.get(TestRoute.CLIENT_AUTH, tags=["test"])
async def fn2():
    return {"Too valid": "✅"}


@route.get(TestRoute.SERVER_AUTH, tags=["test"])
async def fn3():
    return {"Real recognize real frfr": "💯"}
