from datetime import datetime, timezone
from uuid import UUID

from domain.entities.parlay import Parlay, ParlayStatus
from ports.repositories.parlay_repository import ParlayRepository

START_DATETIME = datetime.now(tz=timezone.utc)


def create_parlay(
    token: UUID = "45f79b8f-27e0-413e-9048-552fa2206bde",
    user_token: str = "driver_token",
    event_token: str = "event_token",
    amount: int = 1000,
    status: ParlayStatus = ParlayStatus.PENDING,
    coefficient: float = 1.5,
):
    return Parlay(
        token=token,
        user_token=user_token,
        event_token=event_token,
        amount=amount,
        status=status,
        coefficient=coefficient,
        created_at=datetime.now(tz=timezone.utc),
        status_updated_at=None,
    )


async def create_and_save_parlay(
    repository: ParlayRepository,
    token: UUID = "45f79b8f-27e0-413e-9048-552fa2206bde",
    user_token: str = "user_token",
    event_token: str = "event_token",
    amount: int = 1000,
    status: ParlayStatus = ParlayStatus.PENDING,
    coefficient: float = 1.5,
):
    parlay = Parlay(
        token=token,
        user_token=user_token,
        event_token=event_token,
        amount=amount,
        status=status,
        coefficient=coefficient,
        created_at=datetime.now(tz=timezone.utc),
        status_updated_at=None,
    )
    await repository.save(parlay)
    return parlay
