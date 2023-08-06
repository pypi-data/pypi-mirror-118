import functools
import time
from typing import Optional, Tuple, Callable

from sweelimiter.api.backend import Backend
from sweelimiter.api.interval import Interval

try:
    from asyncio_redis import Connection
except ImportError:
    raise AssertionError('Please install asyncio_redis to use redis_backend')


class AsyncioRedisBackend(Backend):

    async def process(self, key: str, interval: Interval, limit: int) -> Tuple[Optional[str], dict]:
        redis_key = 'limiter_' + key
        r = self._redis()

        time_now = int(time.time_ns() // 1_000_000)

        separation = round(interval.to_miliseconds() / limit)

        await r.setnx(redis_key, '0')
        tat = max(int(await r.get(redis_key)), time_now)

        wait_left = tat - time_now
        est_interval = interval.to_miliseconds() - separation

        if wait_left <= est_interval:
            new_tat = max(tat, time_now) + separation
            await r.set(redis_key, str(new_tat))
            return (None, {
                'key': key,
                'tat': new_tat,
                'separation': separation,
                'wait': wait_left,
                'est_interval': est_interval
            })

        return (f'Hit limiter {key}: {limit} allowed per {interval}', {
            'key': key,
            'tat': tat,
            'separation': separation,
            'wait': wait_left,
            'est_interval': est_interval
        })

    def __init__(self, redis_factory: Callable[[], Connection]):
        self.redis_factory = redis_factory

    @functools.lru_cache(maxsize=None)
    def _redis(self):
        return self.redis_factory()
