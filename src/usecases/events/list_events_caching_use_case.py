from dataclasses import asdict

from domain.entities.event import Event
from ports.api.line_provider import LineProvider
from ports.repositories.event_caching_repository import EventCachingRepository


class ListEventsCachingUseCase:
    def __init__(
        self,
        line_provider_api: LineProvider,
        event_caching_repository: EventCachingRepository,
    ):
        self.line_provider_api = line_provider_api
        self.event_caching_repository = event_caching_repository

    async def __call__(self) -> list[Event] | None:
        if (events := await self.event_caching_repository.get_all_cache()) is None:
            await self.event_caching_repository.remove_all_cache()
            events = await self.__retrieve_events_from_api()
        return events

    async def __retrieve_events_from_api(self) -> list[Event] | None:
        events = await self.line_provider_api.get_active_events()
        for event in events:
            await self.event_caching_repository.set_cache(event.token, asdict(event))
        return events
