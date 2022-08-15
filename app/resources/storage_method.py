from datetime import datetime

import redis

from app.core.config import settings


class LocalStorage:
    def __init__(self) -> None:
        self.storage = {}

    def __contains__(self, key_name):
        return True if key_name in self.storage else False

    def set_key(self, key_name, expire_timestamp):
        timestamp_to_datetime = str(datetime.fromtimestamp(expire_timestamp))
        self.storage[key_name] = timestamp_to_datetime


class RedisStorage:
    def __init__(self):
        self.r = redis.Redis(
            host=settings.REDIS_URL,
            port=settings.REDIS_PORT,
            socket_connect_timeout=settings.REDIS_SOCKET_TIMEOUT,
        )

    def __contains__(self, key_name):
        return self.r.exists(key_name)

    def set_key(self, key_name, expire_timestamp):
        ttl = expire_timestamp - int(datetime.now().timestamp())
        self.r.setex(key_name, ttl, value="Blacklisted token")


storage = LocalStorage() if not settings.REDIS_CONNECTION else RedisStorage()
