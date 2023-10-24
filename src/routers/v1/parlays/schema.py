from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.parlay import LostParlay, Parlay, ParlaysHistory, ParlayStatus, WentInParlay
from routers.v1.parlay.schema import ParlayItem


class WentInParlayItem(BaseModel):
    token: UUID
    user_token: str
    event_token: str
    winnings: float
    status: ParlayStatus
    created_at: datetime


class LostParlayItem(BaseModel):
    token: UUID
    user_token: str
    event_token: str
    loss: float
    status: ParlayStatus
    created_at: datetime


class ParlayHistoryItem(BaseModel):
    type: ParlayStatus
    item: LostParlayItem | WentInParlayItem | ParlayItem

    @classmethod
    def from_entity(cls, event: ParlaysHistory) -> Self:
        return cls(type=event.type, item=cls.__map_to_event_type(event.item))

    @staticmethod
    def __map_to_event_type(item: LostParlay | WentInParlay | Parlay):
        if isinstance(item, LostParlay):
            return LostParlayItem(
                user_token=item.user_token,
                event_token=item.event_token,
                loss=item.loss,
                status=item.status,
                token=item.token,
                created_at=item.created_at,
            )
        if isinstance(item, WentInParlay):
            return WentInParlayItem(
                user_token=item.user_token,
                event_token=item.event_token,
                winnings=item.winnings,
                status=item.status,
                token=item.token,
                created_at=item.created_at,
            )
        return ParlayItem.from_entity(item)


class ParlayHistoryCollection(BaseModel):
    total_count: int = Field(ge=0)
    items: list[ParlayHistoryItem]
    links: dict
