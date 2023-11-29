from fastapi.testclient import TestClient
from starlette import status
from msrv.run import apx
from msrv.settings.urls import URL

client = TestClient(app=apx)


BEARER_TOKEN = "NOTREAL"


def test_is_unauthorized():
    response = client.get(
        url=URL.Test.ServerAuth.PREFIX,
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
