from datetime import timedelta

from domain.entities.event import Event
from ports.repositories.event_caching_repository import EventCachingRepository


class InMemoryEventCachingRepository(EventCachingRepository):
    async def get_cache(self, event_token: str) -> Event | None:
        pass

    async def get_all_cache(self) -> list[Event] | None:
        pass

    async def set_cache(self, event_token: str, response: dict, expire: timedelta = timedelta(minutes=3)) -> bool:
        pass

    async def remove_all_cache(self) -> None:
        pass
