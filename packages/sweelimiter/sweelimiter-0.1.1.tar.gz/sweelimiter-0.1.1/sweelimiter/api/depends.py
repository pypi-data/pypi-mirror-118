from fastapi import Depends, HTTPException
from starlette.requests import Request

from .limit_config import LimitConfig, Limit
from .limiter_engine import LimiterEngine


def create_ratelimit_depends(engine: LimiterEngine):
    def ratelimit(key: str, limits: list[Limit]) -> Depends:
        config = LimitConfig(key, limits)

        async def call(request: Request):
            limit_result = engine.limit(config, request)
            print(limit_result)
            if limit_result.limit_applied:
                raise HTTPException(status_code=429, detail=limit_result.description)

        return Depends(call)

    return ratelimit
