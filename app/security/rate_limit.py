from fastapi_limiter.depends import RateLimiter
from starlette.requests import Request
from starlette.responses import Response

from app.settings.consts import TestRoute

limited_routes = [TestRoute.CLIENT_RATE_LIMITER]


async def rate_limit_check(req: Request, res: Response):
    if req.url.path in limited_routes:
        return await RateLimiter(times=1, seconds=10).__call__(req, res)
