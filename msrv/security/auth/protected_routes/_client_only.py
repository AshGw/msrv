from itertools import chain
from typing import List

from msrv.settings.urls import URL

_test_routes: List[str] = [
    URL.Test.ClientAuth.PREFIX,
    URL.Test.RateLimit.PREFIX,
]

_routes: List[str] = [
    URL.Generate.Free.PREFIX,
    URL.Generate.Hobby.PREFIX,
    URL.Generate.Pro.PREFIX,
]

protected_client_routes: List[str] = list(chain(_routes, _test_routes))
