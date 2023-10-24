from abc import ABC, abstractmethod
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from adapters.connection_engines.redis_engine.redis_engine import RedisEngine
from adapters.connection_engines.sql_alchemy.sql_alchemy import SQLAlchemy
from core.config import get_settings


@lru_cache
def get_sql_alchemy():
    settings = get_settings()
    return SQLAlchemy.start(settings.db_creds)


@lru_cache
def get_redis():
    settings = get_settings()
    return RedisEngine.start(credentials=settings.redis_creds)


class BaseContainer(ABC):
    def __init__(self):
        self.sqlalchemy = get_sql_alchemy()

    async def __aenter__(self):
        session_maker = self.sqlalchemy.session_maker()
        self.db_session = await session_maker.__aenter__()
        self.transaction = self.db_session.begin()
        await self.transaction.__aenter__()
        self.init_dependencies(self.db_session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.transaction.__aexit__(exc_type, exc_val, exc_tb)
        await self.db_session.__aexit__(exc_type, exc_val, exc_tb)

    @abstractmethod
    def init_dependencies(self, db_session: AsyncSession) -> None:
        raise NotImplementedError
