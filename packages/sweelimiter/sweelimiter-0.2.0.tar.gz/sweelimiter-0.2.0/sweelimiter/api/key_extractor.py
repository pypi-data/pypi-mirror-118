from typing import Callable, List

from starlette.requests import Request

KeyExtractorFn = Callable[[Request], List[str]]


class KeyExtractor:
    def __init__(self, prefix: str, fn: KeyExtractorFn):
        self.prefix = prefix
        self.fn = fn

    def extract(self, req: Request) -> List[str]:
        keys = self.fn(req)
        return [f'{self.prefix}{key}' for key in keys]


