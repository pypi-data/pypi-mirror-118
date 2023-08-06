from typing import List

from starlette.requests import Request

from .host_extractor import host_key_extractor
from ..api.key_extractor import KeyExtractor, KeyExtractorFn


def multi_extractor_fn_factory(extractors: List[KeyExtractor]) -> KeyExtractorFn:
    def fn(req: Request) -> List[str]:
        result = []
        for extractor in extractors:
            keys = extractor.extract(req)
            result.extend(keys)
        return result

    return fn


class Extractors:
    @staticmethod
    def multiple(extractors: List[KeyExtractor]):
        return KeyExtractor('', multi_extractor_fn_factory(extractors))

    @staticmethod
    def new(prefix: str, fn: KeyExtractorFn):
        return KeyExtractor(prefix + '@', fn)

    @staticmethod
    def host():
        return host_key_extractor
