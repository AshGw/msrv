import os

import dotenv
from fastapi.testclient import TestClient

from app import apx
from app.settings.consts import TestRoute

dotenv.load_dotenv()
BEARER_TOKEN = os.getenv("SERVER_OAUTH2_TOKEN")

client = TestClient(app=apx)


def test_is_authorized():
    response = client.get(
        url=TestRoute.SERVER_AUTH,
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"},
    )
    assert response.status_code == 200
