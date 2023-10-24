import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from adapters.connection_engines.sql_alchemy.models import Base
from core.settings import TestSettings
from routers.dependencies.redis import RedisDependency


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def engine():
    db_url = URL.create(**TestSettings().db_creds).render_as_string(hide_password=False)
    engine = create_async_engine(db_url)
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def session(engine, create):
    async with AsyncSession(engine) as async_session:
        yield async_session


@pytest_asyncio.fixture(scope="session")
async def redis_session():
    get_redis_engine = RedisDependency()
    engine = get_redis_engine(TestSettings()).redis_engine
    async with engine as session:
        yield session
