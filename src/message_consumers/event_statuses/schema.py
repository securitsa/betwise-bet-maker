from pydantic import BaseModel

from domain.entities.event import EventStatus
from domain.entities.event import EventStatusInput as EventStatusInputEntity


class EventStatusItem(BaseModel):
    token: str
    status: EventStatus

    def to_entity(self) -> EventStatusInputEntity:
        return EventStatusInputEntity(
            token=self.token,
            status=self.status,
        )
