from datetime import datetime

from pydantic import BaseModel, Field

from domain.entities.event import Event, EventStatus


class EventItem(BaseModel):
    token: str
    administrator_token: str
    name: str
    description: str | None
    coefficient: float
    expiration_at: datetime
    status: EventStatus
    created_at: datetime
    status_updated_at: datetime | None

    def to_entity(self) -> Event:
        return Event(
            token=self.token,
            name=self.name,
            description=self.description,
            coefficient=self.coefficient,
            expiration_at=self.expiration_at,
            status=self.status,
            created_at=self.created_at,
            status_updated_at=self.status_updated_at,
        )


class EventsCollection(BaseModel):
    total_count: int = Field(ge=0)
    items: list[EventItem]
    links: dict
