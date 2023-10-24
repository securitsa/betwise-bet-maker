from domain.entities.event import EventStatus, EventStatusInput
from domain.entities.parlay import ParlayStatus
from ports.repositories.parlay_repository import ParlayRepository


class UpdateParlayStatusUseCase:
    def __init__(
        self,
        parlay_repository: ParlayRepository,
    ):
        self.parlay_repository = parlay_repository

    async def __call__(self, event_status_item: EventStatusInput) -> None:
        parlays = await self.parlay_repository.find_by_event_token(event_status_item.token)
        for parlay in parlays:
            parlay.status = await self.__get_parlay_status(event_status_item.status)
            await self.parlay_repository.save(parlay)

    @staticmethod
    async def __get_parlay_status(event_status: EventStatus) -> ParlayStatus:
        statuses = {
            EventStatus.SCHEDULED: ParlayStatus.PENDING,
            EventStatus.LEFT_VICTORY: ParlayStatus.LOST,
            EventStatus.RIGHT_VICTORY: ParlayStatus.WENT_IN,
        }
        return statuses[event_status]
