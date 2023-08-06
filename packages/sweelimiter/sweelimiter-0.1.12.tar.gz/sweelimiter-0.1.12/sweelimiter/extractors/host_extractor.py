from typing import List

from starlette.requests import Request

from sweelimiter.api.key_extractor import new_extractor


def _host_key_extractor(req: Request) -> List[str]:
    return [req.client.host]


host_key_extractor = new_extractor(
    'host',
    _host_key_extractor
)
