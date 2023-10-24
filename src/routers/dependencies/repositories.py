from fastapi import Depends

from adapters.repositories.event_caching_repository.redis_event_caching_repository import RedisRequestCachingRepository
from adapters.repositories.parlay_repository.sqlalchemy_parlay_repository import SQLAlchemyParlayRepository
from ports.repositories.event_caching_repository import EventCachingRepository
from ports.repositories.parlay_repository import ParlayRepository
from routers.dependencies.database import get_db
from routers.dependencies.redis import get_redis


def get_parlay_repository(db=Depends(get_db)) -> ParlayRepository:
    return SQLAlchemyParlayRepository(db)


def get_event_caching_repository(redis=Depends(get_redis)) -> EventCachingRepository:
    return RedisRequestCachingRepository(redis)
