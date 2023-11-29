from typing import Dict, List

from fastapi import APIRouter, Body
from pydantic import BaseModel, EmailStr
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from msrv.security.auth.jwts import jwt_encode
from msrv.settings.urls import URL


class UserEmail(BaseModel):
    email: EmailStr = Body(min_length=11, max_length=335)


router = APIRouter()


fake_aah_mongo_db: List[Dict[str, Dict[str, str]]] = [
    {"x@gmail.com": {"plan": "free"}},
    {"excommunicado@gmail.com": {"plan": "pro"}},
    {"psx@gmail.com": {"plan": "pro"}},
    {"me@gmail.com": {"plan": "hobby"}},
]


@router.patch(path=URL.Token.Client.Refresh.PREFIX, tags=["client", "token"])
async def get_token(email: UserEmail):
    user_email = email.email
    for user_object in fake_aah_mongo_db:
        if user_email in user_object:
            plan = list(user_object.values())[0].get("plan")
            token = jwt_encode(email=user_email, scope={"client": plan})
            return JSONResponse(content={"token": token}, status_code=200)
    raise HTTPException(detail="Unauthorized", status_code=401)
