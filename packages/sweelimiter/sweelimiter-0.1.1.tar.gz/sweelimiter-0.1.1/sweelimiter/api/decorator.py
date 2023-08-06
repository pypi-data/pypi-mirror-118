from functools import wraps

from fastapi import HTTPException
from starlette.requests import Request

from .limiter_engine import LimiterEngine
from .limit_config import LimitConfig, Limit


def create_ratelimit_decorator(engine: LimiterEngine):
    def ratelimit(key: str, limits: list[Limit]):
        config = LimitConfig(key, limits)

        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                limit_result = engine.limit(config, request)
                print(limit_result)
                if limit_result.limit_applied:
                    raise HTTPException(status_code=429, detail=limit_result.description)

                await func(request, *args, **kwargs)

            return wrapper

        return decorator

    return ratelimit
