from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

from domain.entities.parlay import Parlay, ParlayStatus


class ParlayInput(BaseModel):
    event_token: str
    amount: float

    @field_validator("amount")
    def validate_amount(cls, value):
        if round(value, 2) != value:
            raise ValueError("Amount should have at most 2 decimal places")
        return value

    def to_entity(self, user_token: str) -> Parlay:
        return Parlay(
            user_token=user_token,
            event_token=self.event_token,
            amount=int(self.amount * 100),
        )


class ParlayItem(BaseModel):
    token: UUID
    user_token: str
    event_token: str
    amount: float
    coefficient: float
    possible_gain: float
    status: ParlayStatus
    created_at: datetime
    status_updated_at: datetime | None

    @classmethod
    def from_entity(cls, parlay: Parlay):
        return cls(
            token=parlay.token,
            event_token=parlay.event_token,
            user_token=parlay.user_token,
            amount=parlay.amount * 0.01,
            coefficient=parlay.coefficient,
            possible_gain=round(parlay.amount * parlay.coefficient * 0.01, 2),
            status=parlay.status,
            created_at=parlay.created_at,
            status_updated_at=parlay.status_updated_at,
        )
