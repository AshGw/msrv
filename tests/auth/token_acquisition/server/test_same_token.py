from fastapi.testclient import TestClient

from msrv.run import apx
from msrv.settings.urls import URL
from msrv.lib.env import Env

current_env = Env.CURRENT_ENVIRONMENT
BEARER_TOKEN = (
    Env.Dev.SERVER_OAUTH2_TOKEN
    if current_env == "development"
    else Env.Prod.SERVER_OAUTH2_TOKEN
)

client = TestClient(app=apx)


def test_token_is_same():
    response = client.patch(
        url=URL.Token.Server.PREFIX,
        json={"next": False},
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"},
    )
    assert response.json().get("is_new") is False
