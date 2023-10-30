import pytest
import requests

from app.lib.parallelism.main import Executioner
from app.settings.consts import TestRoute

PORT = "80"


def send():
    url = f"http://localhost:{PORT}{TestRoute.CLIENT_RATE_LIMITER}"
    return requests.get(url)


def bombard():
    Executioner.cores_limited_multiprocessor(
        [send, send, send, send, send, send, send, send, send, send]
    )


def app_run() -> bool:
    try:
        url = f"http://localhost:{PORT}"
        response = requests.get(url, headers={"Authorization": f"Bearer x"})
        if response.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        return False


skip_if_app_not_running = pytest.mark.skipif(not app_run(), reason="App is not running")


@skip_if_app_not_running
def test_rate_limited():
    bombard()
    assert send().status_code == 429
