import os

import dotenv
from fastapi.testclient import TestClient

from app import apx
from app.settings.consts import Route

dotenv.load_dotenv()
BEARER_TOKEN = os.getenv("SERVER_OAUTH2_TOKEN")

client = TestClient(app=apx)


def test_token_is_same():
    response = client.patch(
        url=Route.SERVER_TOKEN_GENERATE,
        json={"next": False},
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"},
    )
    assert response.json().get("is_new") is False
