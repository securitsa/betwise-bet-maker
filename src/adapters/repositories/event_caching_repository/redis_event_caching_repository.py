import logging
from datetime import timedelta

from redis.asyncio import Redis
from redis.exceptions import RedisError

from adapters.repositories.event_caching_repository.redis_event_caching_repository_mapper import (
    RedisEventCachingRepositoryMapper,
)
from adapters.repositories.event_caching_repository.utils import deserialize_json, serialize_json
from domain.entities.event import Event
from ports.repositories.event_caching_repository import EventCachingRepository

logger = logging.getLogger()


class RedisRequestCachingRepository(EventCachingRepository):
    prefix = "event-cache:"

    def __init__(self, redis: Redis):
        self.redis = redis
        self.mapper = RedisEventCachingRepositoryMapper()

    async def get_cache(self, event_token: str) -> Event | None:
        try:
            if response := await self.redis.get(self.prefix + ":" + event_token):
                return self.mapper.to_event_entity(deserialize_json(response))
        except RedisError as e:
            logger.exception(e)

    async def get_all_cache(self) -> list[Event] | None:
        try:
            if response := await self.redis.mget(await self.redis.keys("*")):
                return [self.mapper.to_event_entity(deserialize_json(item)) for item in response]
        except RedisError as e:
            logger.exception(e)

    async def set_cache(self, event_token: str, response: dict, expire: timedelta = timedelta(minutes=3)) -> bool:
        try:
            return await self.redis.setex(self.prefix + ":" + event_token, expire, serialize_json(response))
        except (RedisError, TypeError) as e:
            logger.exception(e)

    async def remove_all_cache(self) -> None:
        try:
            await self.redis.flushdb()
        except RedisError as e:
            logger.exception(e)
