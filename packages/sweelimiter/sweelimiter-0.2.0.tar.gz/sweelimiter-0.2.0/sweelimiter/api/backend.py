from abc import ABC, abstractmethod
from typing import Optional, Tuple

from sweelimiter.api.interval import Interval


class Backend(ABC):

    @abstractmethod
    async def process(self, key: str, interval: Interval, limit: int) -> Tuple[Optional[str], dict]:
        pass


class CountingBackend(Backend):

    async def process(self, key: str, interval: Interval, limit: int) -> Tuple[Optional[str], dict]:
        requests_made = self.get_and_increment(key, interval, limit)
        meta = {
            'key': key,
            'requests_made': requests_made,
            'max_requests': limit,
            'requests_left': limit - requests_made
        }

        result = None
        if requests_made > limit:
            result = f'Hit limiter {key}: {limit} allowed per {interval}'

        return result, meta

    @abstractmethod
    def get_and_increment(self, key: str, interval: Interval, limit: int) -> int:
        pass
