from fastapi import Depends, HTTPException
from fastapi.requests import Request

from msrv.lib.env import Env
from msrv.security.auth._scheme import scheme
from msrv.security.auth._verfier import verify_client_token, verify_server_token

from msrv.security.auth.protected_routes import (
    protected_client_routes,
    protected_server_routes,
)


_debug: bool = True if Env.CURRENT_ENVIRONMENT == "development" else False


def check_auth(req: Request, token: str = Depends(scheme)) -> None:
    _yeeted: str = "Unauthorized"
    if req.url.path in protected_server_routes:
        if not verify_server_token(token):
            detail: str = "Only Server Allowed" if _debug else _yeeted
            raise HTTPException(status_code=401, detail=detail)
        ...  # this will raise an unauthorized response by default ove the whole msrv if user
        # doesn't have a bearer token
    if req.url.path in protected_client_routes:
        if not verify_client_token(token):
            detail: str = "Only Authorized Clients Allowed" if _debug else _yeeted
            raise HTTPException(
                status_code=401,
                detail=detail,
            )
        ...  # same as above
    # TODO: SETUP AUTH SCOPES LATER
