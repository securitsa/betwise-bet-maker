from abc import ABC, abstractmethod

from domain.entities.event import Event


class LineProvider(ABC):
    @abstractmethod
    async def get_active_events(self) -> list[Event]:
        pass
