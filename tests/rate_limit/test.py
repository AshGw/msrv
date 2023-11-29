import pytest
import requests

from parallelexec import ParallelExec
from msrv.settings.urls import URL
from starlette import status


PORT = "8000"


def send():
    url = f"http://localhost:{PORT}{URL.Test.RateLimit.PREFIX}"
    return requests.get(url)


def bombard():
    ParallelExec.cores_limited_processor(
        [send, send, send, send, send, send, send, send, send, send]
    )


def app_run() -> bool:
    try:
        url = f"http://localhost:{PORT}"
        response = requests.get(url, headers={"Authorization": "Bearer x"})
        if response.status_code == 200:
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False


skip_if_app_not_running = pytest.mark.skipif(not app_run(), reason="App is not running")


@skip_if_app_not_running
def test_rate_limited():
    bombard()
    assert send().status_code == status.HTTP_429_TOO_MANY_REQUESTS
