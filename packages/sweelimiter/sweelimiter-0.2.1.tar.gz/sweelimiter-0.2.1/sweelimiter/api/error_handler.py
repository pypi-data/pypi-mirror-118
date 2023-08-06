from typing import Optional, Union, Callable, Type

from sweelimiter.api.limiter_result import LimiterResult

ErrorHandlerFn = Callable[[LimiterResult], None]
ExceptionFactory = Callable[[LimiterResult], Exception]


def factory_to_handler_fn(factory: ExceptionFactory) -> ErrorHandlerFn:
    def handler_fn(result) -> None:
        raise factory(result)

    return handler_fn


class ErrorHandler:

    def __init__(self, handler_fn: ErrorHandlerFn):
        self._fn = handler_fn

    def handle(self, result: LimiterResult):
        self._fn(result)


class ErrorHandlers:

    @staticmethod
    def raise_exception(factory: ExceptionFactory):
        return ErrorHandler(factory_to_handler_fn(factory))

    @staticmethod
    def consume(fn: ErrorHandlerFn):
        return ErrorHandler(fn)
