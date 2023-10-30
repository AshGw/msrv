from typing import List

from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.lib.funcs.cpu_watch import overload_check
from app.routes.test.main import route as test_route
from app.security.cors import options
from app.security.oauth2 import check_oauth2_token
from app.security.rate_limit import rate_limit_check
from app.settings.startup import start_event


class ASCM:
    def __init__(
        self,
    ) -> None:
        self.app = FastAPI()

    def enable(
        self,
        *,
        oauth2: bool = False,
        cors: bool = False,
        overload_watch: bool = False,
        rate_limits: bool = False
    ) -> "ASCM":
        dependencies = []
        if rate_limits:
            dependencies.append(Depends(rate_limit_check))
        if oauth2:
            dependencies.append(Depends(check_oauth2_token))
        if overload_watch:
            dependencies.append(Depends(overload_check))
        self.app = FastAPI(dependencies=dependencies, lifespan=start_event)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=options["origins"],
            allow_credentials=options["credentials"],
            allow_methods=options["methods"],
            allow_headers=options["headers"],
        ) if cors else ...
        return self

    def _include_routes(self):
        routes: List[APIRouter] = [
            test_route,
        ]
        for route in routes:
            self.app.include_router(route)

    def build(self) -> FastAPI:
        self._include_routes()
        return self.app
