from itertools import chain
from typing import List

from msrv.settings.urls import URL

_test_routes: List[str] = [URL.Test.ServerAuth.PREFIX]


_routes: List[str] = [
    URL.Token.Server.PREFIX,
    URL.Generate.Server.PREFIX,
]


protected_server_routes: List[str] = list(chain(_routes, _test_routes))
