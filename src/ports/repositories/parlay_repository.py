from abc import ABC, abstractmethod
from typing import Unpack

from domain.entities.parlay import Parlay
from usecases.enum_models import Ordering, ParlayFilters, ParlaySorting


class ParlayRepository(ABC):
    @abstractmethod
    async def save(self, parlay: Parlay) -> Parlay:
        pass

    @abstractmethod
    async def find_by_token(self, token: str) -> Parlay:
        pass

    @abstractmethod
    async def exists(self, token: str) -> bool:
        pass

    @abstractmethod
    async def find_by_event_token(self, token: str) -> list[Parlay]:
        pass

    @abstractmethod
    async def list(
        self,
        page: int = 1,
        limit: int = 50,
        sort_by: ParlaySorting = ParlaySorting.BY_CREATION_DATE,
        order_by: Ordering = Ordering.ASC,
        **filters: Unpack[ParlayFilters],
    ) -> list[Parlay]:
        pass

    @abstractmethod
    async def count(self, **filters: Unpack[ParlayFilters]) -> int:
        pass
