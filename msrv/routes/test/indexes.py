from msrv.settings.urls import URL
from msrv.lib.env import Env
from fastapi import APIRouter

route = APIRouter()


@route.get(URL.Test.RateLimit.PREFIX, tags=["test"])
async def fn1():
    return {"Homie almost yeeted out": "😥"}


@route.get(URL.Test.ClientAuth.PREFIX, tags=["test"])
async def fn2():
    return {"Too valid": "✅"}


@route.get(URL.Test.ServerAuth.PREFIX, tags=["test"])
async def fn3():
    return {"Real recognize real frfr": "💯"}


#########################################################################################################
# whatever under this line is for testing functions only, those are meant to be deleted later.


if Env.CURRENT_ENVIRONMENT == "development":
    pass
