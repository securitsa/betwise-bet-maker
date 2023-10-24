from redis.asyncio import Redis, from_url

from ports.connection_engine import ConnectionEngine


class RedisEngine(ConnectionEngine):
    def __init__(self, redis_engine: Redis):
        self.redis_engine = redis_engine

    @classmethod
    def start(cls, credentials: dict):
        redis_engin = from_url(
            f"redis://:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['database']}"
        )
        return cls(redis_engin)
