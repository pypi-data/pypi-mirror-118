from typing import Optional, Union, Callable, Type

from sweelimiter.api.limiter_result import LimiterResult

LimiterErrorHandler = Optional[Union[Callable[[LimiterResult], None], Type[Exception]]]
