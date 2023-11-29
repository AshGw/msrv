from fastapi.testclient import TestClient
from starlette import status
from msrv.run import apx
from msrv.settings.urls import URL
from msrv.lib.env import Env


client = TestClient(app=apx)

current_env = Env.CURRENT_ENVIRONMENT
token = (
    Env.Dev.CLIENT_OAUTH2_TOKEN
    if current_env == "development"
    else Env.Prod.CLIENT_OAUTH2_TOKEN
)

client = TestClient(app=apx)


PATH: str = URL.Generate.Free.PREFIX


def test_raw_image():
    response = client.post(
        url=PATH,
        json={"prompt": "landscape of "},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/jpeg"


def test_encoded_response():
    response = client.post(
        url=PATH + "/?encode=true",
        json={"prompt": "landscape of "},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "encoded" in response.json()
    assert "prompt" in response.json()
    assert type(response.json().get("image")) is str


def test_blocking_unauthorized():
    response = client.post(
        url=PATH + "/?encode=true",
        json={"prompt": "landscape of "},
        headers={"Authorization": "Bearer Quandale_Dingle"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
