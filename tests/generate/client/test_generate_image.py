import os

import dotenv
from fastapi.testclient import TestClient

from app import apx
from app.settings.consts import Route

dotenv.load_dotenv()
BEARER_TOKEN = os.getenv("CLIENT_OAUTH2_TOKEN")

client = TestClient(app=apx)


def test_raw_image():
    response = client.post(
        url=Route.CLIENT_GENERATE,
        json={"prompt": "landscape of "},
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_encoded_response():
    response = client.post(
        url=Route.CLIENT_GENERATE + "/?encode=true",
        json={"prompt": "landscape of "},
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"},
    )

    assert response.status_code == 200
    assert "encoded" in response.json()
    assert "prompt" in response.json()
    assert type(response.json().get("image")) is str


def test_blocking_unauthorized():
    response = client.post(
        url=Route.CLIENT_GENERATE + "/?encode=true",
        json={"prompt": "landscape of "},
        headers={"Authorization": f"Bearer Quandale_Dingle"},
    )
    assert response.status_code == 401
