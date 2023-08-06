"""
For using redis more easily.
"""
__version__ = "0.1.0"
__name__ = "k3redisutil"

from .redisutil import (
    get_client,
    wait_serve,
    normalize_ip_port,

    RedisChannel,
)

from .redis_proxy_cli import (
    KeyNotFoundError,
    RedisProxyError,
    SendRequestError,
    ServerResponseError,

    RedisProxyClient,
)

__all__ = [
    'get_client',
    'wait_serve',
    'normalize_ip_port',

    'RedisChannel',

    'KeyNotFoundError',
    'RedisProxyError',
    'SendRequestError',
    'ServerResponseError',

    'RedisProxyClient',
]
