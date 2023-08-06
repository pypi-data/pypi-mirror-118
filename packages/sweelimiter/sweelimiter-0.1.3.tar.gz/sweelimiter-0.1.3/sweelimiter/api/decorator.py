from functools import wraps

from fastapi import HTTPException
from starlette.requests import Request

from .limiter import LimiterErrorHandler
from .limiter_engine import LimiterEngine
from .limit_config import LimitConfig, Limit


def create_ratelimit_decorator(engine: LimiterEngine, error_handler: LimiterErrorHandler):
    def ratelimit(key: str, limits: list[Limit]):
        config = LimitConfig(key, limits)

        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                limit_result = await engine.limit(config, request)
                print(limit_result)

                if limit_result.limit_applied:
                    if error_handler:
                        error_handler(limit_result)
                    else:
                        raise HTTPException(status_code=429, detail=limit_result.description)

                await func(request, *args, **kwargs)

            return wrapper

        return decorator

    return ratelimit
