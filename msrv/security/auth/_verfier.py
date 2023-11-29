from msrv.lib.env import Env

SERVER_OAUTH2_TOKEN = (
    Env.Dev.SERVER_OAUTH2_TOKEN
    if Env.CURRENT_ENVIRONMENT == "development"
    else Env.Prod.CLIENT_OAUTH2_TOKEN
)
CLIENT_OAUTH2_TOKEN = (
    Env.Dev.CLIENT_OAUTH2_TOKEN
    if Env.CURRENT_ENVIRONMENT == "development"
    else Env.Prod.CLIENT_OAUTH2_TOKEN
)


def verify_server_token(token: str) -> bool:
    if token == SERVER_OAUTH2_TOKEN:
        return True
    return False


def verify_client_token(token: str) -> bool:
    if token == CLIENT_OAUTH2_TOKEN:
        return True
    return False
