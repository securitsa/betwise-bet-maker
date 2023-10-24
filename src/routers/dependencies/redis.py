from fastapi import Depends

from adapters.connection_engines.redis_engine.redis_engine import RedisEngine
from core.config import get_settings
from core.settings import BaseSettings


class RedisDependency:
    def __init__(self):
        self.redis_engine = None

    def __call__(self, settings: BaseSettings = Depends(get_settings)) -> RedisEngine:
        if not self.redis_engine:
            self.redis_engine = RedisEngine.start(credentials=settings.redis_creds)
        return self.redis_engine


get_redis_engine = RedisDependency()


async def get_redis(redis_engine: RedisEngine = Depends(get_redis_engine)):
    async with redis_engine.redis_engine as session:
        yield session
