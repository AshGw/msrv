import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer

from app.settings.consts import Route, TestRoute

load_dotenv()

SERVER_OAUTH2_TOKEN = os.getenv("SERVER_OAUTH2_TOKEN")
CLIENT_OAUTH2_TOKEN = os.getenv("CLIENT_OAUTH2_TOKEN")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

server_only_routes = [
    Route.SERVER_GENERATE,
    Route.SERVER_TOKEN_GENERATE,
    TestRoute.SERVER_AUTH,
]
authorized_clients_only_routes = [
    Route.CLIENT_GENERATE,
    TestRoute.CLIENT_AUTH,
    TestRoute.CLIENT_RATE_LIMITER,
]


def check_oauth2_token(req: Request, token: str = Depends(oauth2_scheme)):
    if req.url.path in server_only_routes:
        if token != SERVER_OAUTH2_TOKEN:
            raise HTTPException(
                status_code=401, detail="Unauthorized | Only Server Allowed"
            )
    if req.url.path in authorized_clients_only_routes:
        if token != CLIENT_OAUTH2_TOKEN:
            raise HTTPException(
                status_code=401, detail="Unauthorized | Only Authorized Clients Allowed"
            )
    # TODO: SETUP AUTH SCOPES LATER
