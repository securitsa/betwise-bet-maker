import uuid

import pytest
import pytest_asyncio
from sqlalchemy import delete, select

from adapters.connection_engines.sql_alchemy import models
from adapters.repositories.parlay_repository.sqlalchemy_parlay_repository import SQLAlchemyParlayRepository
from core.exceptions.parlay_exceptions import ParlayNotFoundException
from domain.entities.parlay_statistics import ParlayStatistics
from ports.repositories.parlay_repository import ParlayRepository
from tests.utils import create_and_save_parlay


@pytest_asyncio.fixture
async def repository(session) -> ParlayRepository:
    yield SQLAlchemyParlayRepository(session)
    await session.execute(delete(models.ParlaysORM))


@pytest.mark.asyncio
async def test_save_parlay_success(repository, session):
    parlay = await create_and_save_parlay(repository=repository)
    result = await session.execute(select(models.ParlaysORM))
    parlays_db = result.scalars().all()
    assert len(parlays_db) == 1
    assert str(parlays_db[0].event_token) == parlay.event_token


@pytest.mark.asyncio
async def test_find_parlay_success(repository):
    parlay = await create_and_save_parlay(repository=repository)
    parlay_db = await repository.find_by_token(parlay.token)
    assert parlay_db.event_token == parlay.event_token


@pytest.mark.asyncio
async def test_find_parlay_not_found(repository):
    with pytest.raises(ParlayNotFoundException):
        await repository.find_by_token(str(uuid.uuid4()))


@pytest.mark.asyncio
async def test_get_user_parlay_statistics_with_no_data(repository):
    stat = await repository.get_user_parlays_statistics("user_token")
    assert stat == ParlayStatistics()


@pytest.mark.asyncio
async def test_get_user_parlay_statistics_success(repository):
    for i in range(5):
        await create_and_save_parlay(
            repository=repository,
            token=uuid.uuid4(),
        )
    stat = await repository.get_user_parlays_statistics("user_token")
    assert stat == ParlayStatistics(
        parlays_count=5,
        went_in_parlays_count=0,
        lost_parlays_count=0,
        number_of_processors=5,
        winning_percentage=0,
        overall_win=0,
        overall_loss=0,
    )


@pytest.mark.asyncio
async def test_get_parlay_statistics_with_no_data(repository):
    stat = await repository.get_total_parlays_statistics()
    assert stat == ParlayStatistics()


@pytest.mark.asyncio
async def test_get_parlay_statistics_success(repository):
    for i in range(5):
        await create_and_save_parlay(
            repository=repository,
            token=uuid.uuid4(),
        )
    stat = await repository.get_total_parlays_statistics()
    assert stat == ParlayStatistics(
        parlays_count=5,
        went_in_parlays_count=0,
        lost_parlays_count=0,
        number_of_processors=5,
        winning_percentage=0,
        overall_win=0,
        overall_loss=0,
    )
