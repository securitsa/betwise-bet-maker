from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class ParlayStatus(StrEnum):
    PENDING = "pending"
    WENT_IN = "went_in"
    LOST = "lost"


@dataclass
class Parlay:
    user_token: str
    event_token: str
    amount: int
    status: ParlayStatus | None = None
    coefficient: float | None = None
    token: UUID | None = None
    created_at: datetime | None = field(default=None, compare=False)
    status_updated_at: datetime | None = field(default=None, compare=False)


@dataclass
class WentInParlay:
    user_token: str
    event_token: str
    winnings: float
    status: ParlayStatus
    token: UUID
    created_at: datetime


@dataclass
class LostParlay:
    user_token: str
    event_token: str
    loss: float
    status: ParlayStatus
    token: UUID
    created_at: datetime


@dataclass
class ParlaysHistory:
    type: ParlayStatus
    item: Parlay | WentInParlay | LostParlay
