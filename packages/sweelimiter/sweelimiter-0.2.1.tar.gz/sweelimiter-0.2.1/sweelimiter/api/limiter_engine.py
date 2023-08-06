from typing import List, Union

from starlette.requests import Request

from .backend import Backend
from .bypass_checker import BypassChecker
from .key_extractor import KeyExtractor
from .limit_config import LimitConfig
from .limiter_result import LimiterResult


class LimiterEngine:

    def __init__(
            self,
            extractor: KeyExtractor,
            backend: Backend,
            bypass_checkers: List[BypassChecker] = None,
            prefix: str = 'global',
    ):
        self._prefix = prefix
        self._extractor = extractor
        self._backend = backend

        if not bypass_checkers:
            bypass_checkers = []

        self._bypass_checkers = bypass_checkers

    def _is_bypassed(self, req: Request) -> bool:
        if any(checker(req) for checker in self._bypass_checkers):
            return True
        else:
            return False

    async def limit(self, config: LimitConfig, req: Request) -> LimiterResult:
        if self._is_bypassed(req):
            return LimiterResult(False, 'Bypassed', [])

        limiter_meta = []
        error_hit: Union[LimiterResult, None] = None

        for req_key in self._extractor.extract(req):

            for limit in config.limits:
                full_key = f'{self._prefix}@{config.key}@{req_key}@{int(limit.interval.to_miliseconds())}'

                error, meta = await self._backend.process(full_key, limit.interval, limit.max_requests)

                limiter_meta.append(meta)

                if error is not None:
                    error_hit = LimiterResult(True, error, limiter_meta)

        if error_hit:
            return error_hit

        return LimiterResult(False, 'Limiters not hit', limiter_meta)
