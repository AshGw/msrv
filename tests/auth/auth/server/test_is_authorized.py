from fastapi.testclient import TestClient

from msrv.run import apx
from msrv.settings.urls import URL
from msrv.lib.env import Env


client = TestClient(app=apx)

current_env = Env.CURRENT_ENVIRONMENT
token = (
    Env.Dev.SERVER_OAUTH2_TOKEN
    if current_env == "development"
    else Env.Prod.SERVER_OAUTH2_TOKEN
)

client = TestClient(app=apx)


def test_is_authorized():
    response = client.get(
        url=URL.Test.ServerAuth.PREFIX,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
