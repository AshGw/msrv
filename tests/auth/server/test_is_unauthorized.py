from fastapi.testclient import TestClient

from app import apx
from app.settings.consts import TestRoute

client = TestClient(app=apx)


BEARER_TOKEN = "NOTREAL"


def test_is_unauthorized():
    response = client.get(
        url=TestRoute.SERVER_AUTH,
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"},
    )
    assert response.status_code == 401
