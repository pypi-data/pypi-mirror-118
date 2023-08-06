from typing import Optional, Tuple

from sweelimiter.api.backend import Backend

try:
    from asyncio_redis import Connection
except ImportError:
    raise AssertionError('Please install asyncio_redis to use redis_backend')


class AsyncioRedisBackend(Backend):

    async def process(self, key: str, interval_ms: int, limit: int) -> Tuple[Optional[str], dict]:
        redis_key = 'limiter_' + key
        r = self.r

        seconds, microseconds = await r.time()
        time_now = int(seconds * 1000 + microseconds / 1000)

        separation = round(interval_ms / limit)

        await r.setnx(redis_key, 0)
        tat = max(int(await r.get(redis_key)), time_now)

        wait_left = tat - time_now
        est_interval = interval_ms - separation

        if wait_left <= est_interval:
            new_tat = max(tat, time_now) + separation
            await r.set(redis_key, new_tat)
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

    def __init__(self, r: Connection):
        self.r = r
