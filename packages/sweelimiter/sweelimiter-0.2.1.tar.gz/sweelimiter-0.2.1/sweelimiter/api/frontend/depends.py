from typing import List

from fastapi import Depends, HTTPException
from starlette.requests import Request

from sweelimiter.api.limit_config import LimitConfig, Limit
from sweelimiter.api.error_handler import ErrorHandler
from sweelimiter.api.limiter_engine import LimiterEngine


def create_ratelimit_depends(engine: LimiterEngine, error_handler: ErrorHandler):
    def ratelimit(key: str, *args: Limit) -> Depends:
        config = LimitConfig(key, args)

        async def call(request: Request):
            limit_result = await engine.limit(config, request)
            # print(limit_result)

            if limit_result.limit_applied:
                if error_handler:
                    error_handler.handle(limit_result)
                else:
                    raise HTTPException(status_code=429, detail=limit_result.description)

        return Depends(call)

    return ratelimit
