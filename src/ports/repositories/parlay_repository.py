from abc import ABC, abstractmethod

from domain.entities.parlay import Parlay
from domain.entities.parlay_statistics import ParlayStatistics


class ParlayRepository(ABC):
    @abstractmethod
    async def save(self, parlay: Parlay) -> Parlay:
        pass

    @abstractmethod
    async def find_by_token(self, token: str) -> Parlay:
        pass

    @abstractmethod
    async def find_by_event_token(self, token: str) -> list[Parlay]:
        pass

    @abstractmethod
    async def get_total_parlays_statistics(self) -> ParlayStatistics:
        pass

    @abstractmethod
    async def get_user_parlays_statistics(self, user_token) -> ParlayStatistics:
        pass
