from typing import Optional, Callable, Union, Type

from .depends import create_ratelimit_depends
from .limiter_engine import LimiterEngine
from .decorator import create_ratelimit_decorator
from .limiter_result import LimiterResult

LimiterErrorHandler = Optional[Union[Callable[[LimiterResult], None], Type[Exception]]]


class Limiter:

    def __init__(
            self,
            engine: LimiterEngine,
            error_handler: LimiterErrorHandler
    ):
        self.engine = engine
        self.error_handler = error_handler

    @property
    def decorator(self):
        return create_ratelimit_decorator(self.engine, self.error_handler)

    @property
    def depends(self):
        return create_ratelimit_depends(self.engine, self.error_handler)
