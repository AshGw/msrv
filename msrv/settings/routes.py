from typing import List

from fastapi import APIRouter

from msrv.routes.generate.free.index import route as generate_client_free_route
from msrv.routes.generate.srv.index import route as generate_server_route
from msrv.routes.index import route as home_route
from msrv.routes.test.indexes import route as test_route
from msrv.routes.token.server import route as token_server_route
from msrv.routes.token.u.refresh.index import router as token_u_refresh

routes: List[APIRouter] = [
    home_route,
    test_route,
    token_server_route,
    generate_server_route,
    generate_client_free_route,
    token_u_refresh,
]
