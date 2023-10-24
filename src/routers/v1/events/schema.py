from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.event import Event, EventStatus


class EventItem(BaseModel):
    token: UUID
    name: str
    description: str | None
    coefficient: float
    expiration_at: datetime
    status: EventStatus
    created_at: datetime
    status_updated_at: datetime | None

    @classmethod
    def from_entity(cls, event: Event):
        return cls(
            token=event.token,
            name=event.name,
            coefficient=event.coefficient,
            status=event.status,
            created_at=event.created_at,
            description=event.description,
            status_updated_at=event.status_updated_at,
            expiration_at=event.expiration_at,
        )


class EventsCollection(BaseModel):
    total_count: int = Field(ge=0)
    items: list[EventItem]
