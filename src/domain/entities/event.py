from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class EventStatus(StrEnum):
    SCHEDULED = "scheduled"
    RIGHT_VICTORY = "right_victory"
    LEFT_VICTORY = "left_victory"


@dataclass
class Event:
    name: str
    coefficient: float
    expiration_at: datetime
    status: EventStatus
    token: str
    description: str
    created_at: datetime
    status_updated_at: datetime | None = field(default=None, compare=False)
