from abc import ABC, abstractmethod
from typing import Unpack

from domain.entities.parlay import ParlaysHistory
from usecases.enum_models import Ordering, ParlayFilters, ParlaySorting


class UserRepository(ABC):
    @abstractmethod
    async def get_parlays_history(
        self,
        page: int = 1,
        limit: int = 50,
        sort_by: ParlaySorting = ParlaySorting.BY_CREATION_DATE,
        order_by: Ordering = Ordering.ASC,
        **filters: Unpack[ParlayFilters],
    ) -> list[ParlaysHistory]:
        pass

    @abstractmethod
    async def get_parlays_history_count(self, **filters: Unpack[ParlayFilters]) -> int:
        pass
