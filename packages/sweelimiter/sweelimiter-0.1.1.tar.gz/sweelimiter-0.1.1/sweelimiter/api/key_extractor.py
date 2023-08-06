from typing import Callable

from starlette.requests import Request

KeyExtractorFn = Callable[[Request], list[str]]


class KeyExtractor:
    def __init__(self, prefix: str, fn: KeyExtractorFn):
        self.prefix = prefix
        self.fn = fn

    def extract(self, req: Request) -> list[str]:
        keys = self.fn(req)
        return [f'{self.prefix}@{key}' for key in keys]


def new_extractor(prefix: str, fn: KeyExtractorFn):
    return KeyExtractor(prefix, fn)