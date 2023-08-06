from itertools import chain
from typing import Callable, List

from starlette.requests import Request

from .key_extractor import KeyExtractor
from .backend import Backend
from .bypass_checker import BypassChecker
from .limit_config import LimitConfig
from .limiter_result import LimiterResult


class LimiterEngine:

    def __init__(
            self,
            prefix: str,
            extractors: List[KeyExtractor],
            backend: Backend,
            bypass_checkers: List[BypassChecker],
    ):
        self._prefix = prefix
        self._extractors = extractors
        self._backend = backend
        self._bypass_checkers = bypass_checkers

    def _get_all_keys(self, req: Request) -> List[str]:
        keys = list(chain.from_iterable([e.extract(req) for e in self._extractors]))
        return keys

    def _is_bypassed(self, req: Request) -> bool:
        if any(checker(req) for checker in self._bypass_checkers):
            return True
        else:
            return False

    async def limit(self, config: LimitConfig, req: Request) -> LimiterResult:
        if self._is_bypassed(req):
            return LimiterResult(False, 'Bypassed', [])

        limiter_meta = []

        for extractor in self._extractors:
            keys = extractor.extract(req)

            for req_key in keys:

                for limit in config.limits:
                    full_key = f'{self._prefix}@{config.key}@{req_key}@{limit.interval}'

                    error, meta = await self._backend.process(full_key, limit.interval, limit.max_requests)

                    limiter_meta.append(meta)

                    if error is not None:
                        return LimiterResult(True, error, limiter_meta)

        return LimiterResult(False, 'Limiters not hit', limiter_meta)


def create_limiter_engine(
        prefix: str,
        extractors: List[KeyExtractor],
        backend: Backend,
        bypass_checkers: List[BypassChecker] = None,
):
    if bypass_checkers is None:
        bypass_checkers = []

    return LimiterEngine(
        prefix,
        extractors,
        backend,
        bypass_checkers
    )
