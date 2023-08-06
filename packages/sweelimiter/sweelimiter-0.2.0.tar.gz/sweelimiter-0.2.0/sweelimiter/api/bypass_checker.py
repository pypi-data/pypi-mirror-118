from typing import Callable

from starlette.requests import Request

BypassChecker = Callable[[Request], bool]
