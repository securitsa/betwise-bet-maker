from dataclasses import asdict

from core.exceptions.event_exceptions import EventNotFoundException
from domain.entities.event import Event
from domain.entities.parlay import Parlay, ParlayStatus
from ports.api.line_provider import LineProvider
from ports.repositories.event_caching_repository import EventCachingRepository
from ports.repositories.parlay_repository import ParlayRepository


class SaveParlayUseCase:
    def __init__(
        self,
        parlay_repository: ParlayRepository,
        line_provider_api: LineProvider,
        event_caching_repository: EventCachingRepository,
    ):
        self.parlay_repository = parlay_repository
        self.line_provider_api = line_provider_api
        self.event_caching_repository = event_caching_repository

    async def __call__(self, parlay: Parlay) -> Parlay:
        event = await self.__get_event_info(parlay.event_token)
        parlay.event_token = event.token
        parlay.coefficient = event.coefficient
        parlay.status = ParlayStatus.PENDING
        parlay = await self.parlay_repository.save(parlay)
        return parlay

    async def __get_event_info(self, event_token: str) -> Event:
        if (event := await self.event_caching_repository.get_cache(event_token)) is None:
            await self.event_caching_repository.remove_all_cache()
            event = await self.__retrieve_event_from_api(event_token)
        return event

    async def __retrieve_event_from_api(self, event_token: str) -> Event:
        if not (events := await self.line_provider_api.get_active_events()):
            raise EventNotFoundException(event_token)
        for event in events:
            await self.event_caching_repository.set_cache(event.token, asdict(event))
            if event.token == event_token:
                return event
        raise EventNotFoundException(event_token)
