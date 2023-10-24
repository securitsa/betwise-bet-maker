from abc import ABC, abstractmethod
from datetime import timedelta

from domain.entities.event import Event


class EventCachingRepository(ABC):
    @abstractmethod
    async def get_cache(self, event_token: str) -> Event | None:
        pass

    @abstractmethod
    async def set_cache(self, event_token: str, response: dict, expire: timedelta = timedelta(minutes=3)) -> bool:
        pass

    @abstractmethod
    async def remove_all_cache(self) -> None:
        pass
