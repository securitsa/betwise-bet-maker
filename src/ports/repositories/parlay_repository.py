from abc import ABC, abstractmethod

from domain.entities.parlay import Parlay


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
