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
    coefficient: float
    status: ParlayStatus
    token: UUID | None = None
    created_at: datetime | None = field(default=None, compare=False)
    status_updated_at: datetime | None = field(default=None, compare=False)
