from .depends import create_ratelimit_depends
from .limiter_engine import LimiterEngine
from .decorator import create_ratelimit_decorator


class Limiter:

    def __init__(self, engine: LimiterEngine):
        self.engine = engine

    @property
    def decorator(self):
        return create_ratelimit_decorator(self.engine)

    @property
    def depends(self):
        return create_ratelimit_depends(self.engine)
