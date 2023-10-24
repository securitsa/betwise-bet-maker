import logging
from datetime import timedelta

from redis.asyncio import Redis
from redis.exceptions import RedisError

from adapters.repositories.event_caching_repository.utils import deserialize_json, serialize_json
from ports.repositories.event_caching_repository import EventCachingRepository

logger = logging.getLogger()


class RedisRequestCachingRepository(EventCachingRepository):
    prefix = "event-cache:"

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_cache(self, path: str, event_token: str) -> dict | None:
        try:
            if response := await self.redis.get(self.prefix + path + ":" + event_token):
                return deserialize_json(response)
        except RedisError as e:
            logger.exception(e)

    async def set_cache(
        self, path: str, event_token: str, response: dict, expire: timedelta = timedelta(minutes=3)
    ) -> bool:
        try:
            return await self.redis.setex(self.prefix + path + ":" + event_token, expire, serialize_json(response))
        except (RedisError, TypeError) as e:
            logger.exception(e)

    async def remove_all_cache(self) -> None:
        try:
            await self.redis.delete()
        except RedisError as e:
            logger.exception(e)
