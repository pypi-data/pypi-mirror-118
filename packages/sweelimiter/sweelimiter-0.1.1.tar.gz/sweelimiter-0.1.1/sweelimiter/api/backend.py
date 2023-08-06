from abc import ABC, abstractmethod
from typing import Optional


class Backend(ABC):

    @abstractmethod
    def process(self, key: str, interval_ms: int, limit: int) -> tuple[Optional[str], dict]:
        pass


class CountingBackend(Backend):

    def process(self, key: str, interval_ms: int, limit: int) -> tuple[Optional[str], dict]:
        requests_made = self.get_and_increment(key, interval_ms, limit)
        meta = {
            'key': key,
            'requests_made': requests_made,
            'max_requests': limit,
            'requests_left': limit - requests_made
        }

        result = None
        if requests_made > limit:
            result = f'Hit limiter {key}: {limit} allowed per {interval_ms}ms'

        return result, meta

    @abstractmethod
    def get_and_increment(self, key: str, interval_ms: int, limit: int) -> int:
        pass
