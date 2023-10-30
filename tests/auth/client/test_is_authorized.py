import os

import dotenv
from fastapi.testclient import TestClient

from app import apx
from app.settings.consts import TestRoute

dotenv.load_dotenv()
BEARER_TOKEN = os.getenv("CLIENT_OAUTH2_TOKEN")
# TODO: COORDINATE WITH THE FRONT END TO FETCH FROM A COMMON DATABASE

client = TestClient(app=apx)


def test_is_authorized():
    response = client.get(
        url=TestRoute.CLIENT_AUTH,
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"},
    )
    assert response.status_code == 200
