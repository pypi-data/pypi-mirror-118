from typing import Optional

from sweelimiter.api.backend import Backend

try:
    from redis import Redis
except ImportError:
    raise AssertionError('Please install redis to use redis_backend')


class RedisBackend(Backend):

    async def process(self, key: str, interval_ms: int, limit: int) -> tuple[Optional[str], dict]:
        redis_key = 'limiter_' + key
        r = self.r

        seconds, microseconds = r.time()
        time_now = int(seconds * 1000 + microseconds / 1000)

        separation = round(interval_ms / limit)

        r.setnx(redis_key, 0)
        tat = max(int(r.get(redis_key)), time_now)

        wait_left = tat - time_now
        est_interval = interval_ms - separation

        if wait_left <= est_interval:
            new_tat = max(tat, time_now) + separation
            r.set(redis_key, new_tat)
            return (None, {
                'key': key,
                'tat': new_tat,
                'separation': separation,
                'wait': wait_left,
                'est_interval': est_interval
            })

        return (f'Hit limiter {key}: {limit} allowed per {interval_ms}ms, ', {
            'key': key,
            'tat': tat,
            'separation': separation,
            'wait': wait_left,
            'est_interval': est_interval
        })

    def __init__(self, r: Redis):
        self.r = r
