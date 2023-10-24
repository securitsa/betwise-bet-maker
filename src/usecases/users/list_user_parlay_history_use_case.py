from typing import Unpack

from domain.entities.parlay import ParlaysHistory
from ports.repositories.user_repository import UserRepository
from usecases.enum_models import Ordering, ParlayFilters, ParlaySorting


class ListUserParlayHistoryUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(
        self,
        page: int = 1,
        limit: int = 50,
        sort_by: ParlaySorting = ParlaySorting.BY_CREATION_DATE.value,
        order_by: Ordering = Ordering.ASC.value,
        only_active: bool = True,
        **filters: Unpack[ParlayFilters],
    ) -> (list[ParlaysHistory], int):
        events = await self.user_repository.get_parlays_history(page, limit, sort_by, order_by, **filters)
        count = await self.user_repository.get_parlays_history_count(**filters)
        return events, count
