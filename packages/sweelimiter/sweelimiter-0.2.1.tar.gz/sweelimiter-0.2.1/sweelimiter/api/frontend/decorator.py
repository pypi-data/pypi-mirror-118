from functools import wraps
from typing import List

from fastapi import HTTPException
from starlette.requests import Request

from sweelimiter.api.error_handler import ErrorHandlerFn, ErrorHandler
from sweelimiter.api.limiter_engine import LimiterEngine
from sweelimiter.api.limit_config import LimitConfig, Limit


def create_ratelimit_decorator(engine: LimiterEngine, error_handler: ErrorHandler):
    def ratelimit(key: str, *args: Limit):
        config = LimitConfig(key, args)

        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                limit_result = await engine.limit(config, request)

                if limit_result.limit_applied:
                    if error_handler:
                        error_handler.handle(limit_result)
                    else:
                        raise HTTPException(status_code=429, detail=limit_result.description)

                await func(request, *args, **kwargs)

            return wrapper

        return decorator

    return ratelimit
