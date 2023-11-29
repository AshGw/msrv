from fastapi.testclient import TestClient
from starlette import status
from msrv.run import apx
from msrv.settings.urls import URL
from msrv.lib.env import Env

current_env = Env.CURRENT_ENVIRONMENT
BEARER_TOKEN = (
    Env.Dev.SERVER_OAUTH2_TOKEN
    if current_env == "development"
    else Env.Prod.SERVER_OAUTH2_TOKEN
)
SRV_PATH = URL.Generate.Server.PREFIX

client = TestClient(app=apx)


def test_raw_image():
    response = client.post(
        url=SRV_PATH,
        json={"prompt": "landscape of "},
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/jpeg"


def test_encoded_response():
    response = client.post(
        url=SRV_PATH + "/?encode=true",
        json={"prompt": "landscape of "},
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "encoded" in response.json()
    assert "prompt" in response.json()
    assert type(response.json().get("image")) is str


def test_blocking_unauthorized():
    response = client.post(
        url=SRV_PATH + "/?encode=true",
        json={"prompt": "landscape of "},
        headers={"Authorization": "Bearer Quandale_Dingle"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
