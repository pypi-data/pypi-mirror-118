from typing import List, Union
from durations import Duration

from sweelimiter.api.interval import Interval

IntervalArgument = Union[str, Interval, int]


def get_interval(arg: IntervalArgument) -> Interval:
    if type(arg) == str:
        return Interval(arg)
    if type(arg) == int:
        return Interval.of_seconds(arg)
    if type(arg) == Interval:
        return arg
    raise Exception('Invalid interval:', arg)


class Limit:

    def __init__(
            self,
            interval: IntervalArgument,
            max_requests: int
    ):
        self.interval = get_interval(interval)
        self.max_requests = max_requests

    def __repr__(self):
        return f'Limit(interval={self.interval},max_requests={self.max_requests})'


class LimitConfig:

    def __init__(
            self,
            key: str,
            limits: List[Limit],
    ):
        self.key = key
        self.limits = limits

    def __repr__(self):
        return f'LimitConfig(key={self.key},limits={self.limits})'
