from .error_handler import ErrorHandler
from .frontend import create_ratelimit_decorator, create_ratelimit_depends, create_ratelimit_middleware
from .limit_config import LimitConfig
from .limiter_engine import LimiterEngine


class Limiter:

    def __init__(
            self,
            engine: LimiterEngine,
            error_handler: ErrorHandler
    ):
        self.engine = engine
        self.error_handler = error_handler

    @property
    def decorator(self):
        return create_ratelimit_decorator(self.engine, self.error_handler)

    @property
    def depends(self):
        return create_ratelimit_depends(self.engine, self.error_handler)

    def middleware(self, config: LimitConfig):
        return create_ratelimit_middleware(self.engine, self.error_handler, config)
