from typing import Type

from fastapi import HTTPException
from requests import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from sweelimiter.api.error_handler import ErrorHandler
from sweelimiter.api.limit_config import LimitConfig
from sweelimiter.api.limiter_engine import LimiterEngine


def create_ratelimit_middleware(
        engine: LimiterEngine,
        error_handler: ErrorHandler,
        config: LimitConfig
) -> Type[BaseHTTPMiddleware]:
    class LimiterMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

            limit_result = await engine.limit(config, request)

            if limit_result.limit_applied:
                if error_handler:
                    error_handler.handle(limit_result)
                else:
                    raise HTTPException(status_code=429, detail=limit_result.description)

            return await call_next(request)

    return LimiterMiddleware
