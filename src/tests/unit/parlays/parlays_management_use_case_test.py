from datetime import datetime, timezone
from uuid import UUID

import pytest
import pytest_asyncio

from adapters.api.line_provider.fake_line_provider import FakeLineProvider
from adapters.repositories.event_caching_repository.in_memory_event_caching_repository import (
    InMemoryEventCachingRepository,
)
from adapters.repositories.parlay_repository.in_memory_parlay_repository import InMemoryParlayRepository
from core.exceptions.event_exceptions import EventNotFoundException
from core.exceptions.external_exceptions import LineProviderException
from domain.entities.event import EventStatus, EventStatusInput
from domain.entities.parlay import Parlay, ParlayStatus
from usecases.parlays.save_parlay_use_case import SaveParlayUseCase
from usecases.parlays.update_parlay_status_use_case import UpdateParlayStatusUseCase


@pytest_asyncio.fixture()
async def parlay():
    return Parlay(
        token=UUID("3cf68fc8-cb61-480b-b51a-bc0da9245fed"),
        user_token="user_token",
        event_token="event_token",
        status=ParlayStatus.PENDING,
        created_at=datetime.now().replace(tzinfo=timezone.utc),
        amount=1000,
        coefficient=1.7,
    )


@pytest.fixture
def parlay_repository():
    return InMemoryParlayRepository()


@pytest.fixture
def event_caching_repository():
    return InMemoryEventCachingRepository()


@pytest.fixture
def save_parlay_use_case(parlay_repository, event_caching_repository) -> SaveParlayUseCase:
    return SaveParlayUseCase(parlay_repository, FakeLineProvider(), event_caching_repository)


@pytest.fixture
def update_parlay_use_case(parlay_repository) -> UpdateParlayStatusUseCase:
    return UpdateParlayStatusUseCase(parlay_repository)


@pytest.mark.asyncio
async def test_parlay_create_event_not_found(
    parlay_repository: InMemoryParlayRepository,
    save_parlay_use_case: SaveParlayUseCase,
    parlay: Parlay,
):
    with pytest.raises(EventNotFoundException):
        await save_parlay_use_case(parlay=parlay)


@pytest.mark.asyncio
async def test_parlay_create_line_provider_unavailable(
    parlay_repository: InMemoryParlayRepository,
    save_parlay_use_case: SaveParlayUseCase,
    parlay: Parlay,
):
    save_parlay_use_case.line_provider_api.with_error = True
    with pytest.raises(LineProviderException):
        await save_parlay_use_case(parlay=parlay)


@pytest.mark.asyncio
async def test_parlay_update_success(
    parlay_repository: InMemoryParlayRepository,
    update_parlay_use_case: UpdateParlayStatusUseCase,
    parlay: Parlay,
):
    parlay_repository.parlays_data[parlay.token] = parlay
    await update_parlay_use_case(EventStatusInput(EventStatus.LEFT_VICTORY, parlay.event_token))

    assert parlay_repository.parlays_data[parlay.token].status == ParlayStatus.LOST
