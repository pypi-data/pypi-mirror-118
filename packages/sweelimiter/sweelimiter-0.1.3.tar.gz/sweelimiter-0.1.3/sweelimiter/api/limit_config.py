class Limit:

    def __init__(
            self,
            interval: int,
            max_requests: int
    ):
        self.interval = interval
        self.max_requests = max_requests

    def __repr__(self):
        return f'Limit(interval={self.interval},max_requests={self.max_requests})'


class LimitConfig:

    def __init__(
            self,
            key: str,
            limits: list[Limit],
    ):
        self.key = key
        self.limits = limits

    def __repr__(self):
        return f'LimitConfig(key={self.key},limits={self.limits})'
