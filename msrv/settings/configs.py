from typing import List, Optional, Annotated
from typing_extensions import Annotated, Doc  # type: ignore [attr-defined]


from fastapi import Depends, FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from msrv.security.cors import options
from msrv.security.cpu_overload import overload_check
from msrv.security.auth import check_auth
from msrv.security.rate_limiter import rate_limit_check
from msrv.settings.startup import start_event
from msrv.settings.urls import URL
from msrv.settings.routes import routes


class ASCM:
    def __init__(
        self,
    ) -> None:
        self.app = FastAPI()

    def enable(
        self,
        *,
        oauth2: Annotated[
            bool,
            Doc(
                """
                Enables OAuth2 for the specified routes at,
                check /security/auth/protected_routes
                To enable OAuth2 & lockdown the whole msrv set auto_error=False at:
                security/auth/_scheme.py
                """
            ),
        ] = False,
        cors: Annotated[
            bool,
            Doc(
                """
                Enables Cross Origin Resource Sharing for the specified configuration at:
                security/cors/__init__.py
                """
            ),
        ] = False,
        overload_watch: Annotated[
            bool,
            Doc(
                """
                Enables CPU overload watching over the whole msrv to prevent server coming to a halt,
                for configurations check: security/cpu_overload/__init__.py
                """
            ),
        ] = False,
        rate_limits: Annotated[
            bool,
            Doc(
                """
                Enables rate limiting for the routes configured at:
                security/rate_limiter/limited_routes
                """
            ),
        ] = False,
    ) -> "ASCM":
        dependencies = []
        if rate_limits:
            dependencies.append(Depends(rate_limit_check))
        if oauth2:
            dependencies.append(Depends(check_auth))
        if overload_watch:
            dependencies.append(Depends(overload_check))
        self.app = FastAPI(
            dependencies=dependencies,
            lifespan=start_event,
            docs_url=URL.Docs.Swagger.PREFIX,
        )
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=options["origins"],
            allow_credentials=options["credentials"],
            allow_methods=options["methods"],
            allow_headers=options["headers"],
        ) if cors else ...
        return self

    def _include_route(self, route: APIRouter) -> None:
        self.app.include_router(route)

    def _include_all_routes(self) -> None:
        for route in routes:
            self._include_route(route)

    def mount(
        self,
        *,
        specific_routes: Optional[List[APIRouter]] = None,
        all_routes: Optional[bool] = None,
    ) -> "ASCM":
        if specific_routes and all_routes:
            raise ValueError("Can't pick up both")
        if specific_routes:
            for route in specific_routes:
                self._include_route(route)
        if all_routes:
            self._include_all_routes()
        return self

    def build(self) -> FastAPI:
        return self.app
