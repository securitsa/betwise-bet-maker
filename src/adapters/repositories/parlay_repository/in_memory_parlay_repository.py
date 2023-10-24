import copy

from core.exceptions.parlay_exceptions import ParlayNotFoundException
from domain.entities.parlay import Parlay
from ports.repositories.parlay_repository import ParlayRepository


class InMemoryParlayRepository(ParlayRepository):
    parlays_data = {}

    async def save(self, parlay: Parlay):
        self.parlays_data[parlay.token] = copy.deepcopy(parlay)

    async def find_by_token(self, token: str) -> Parlay:
        if token in self.parlays_data:
            return copy.deepcopy(self.parlays_data[token][0])
        raise ParlayNotFoundException

    async def find_by_event_token(self, token: str) -> list[Parlay]:
        return [
            copy.deepcopy(self.parlays_data[parlay_token])
            for parlay_token in self.parlays_data
            if self.parlays_data[parlay_token].event_token == token
        ]

    async def get_total_parlays_statistics(self):
        return self.__calculate_parlays_statistics()

    async def get_user_parlays_statistics(self, user_token: str):
        return self.__calculate_parlays_statistics(user_token)

    def __calculate_parlays_statistics(self, user_token: str = None):
        parlays = self.parlays_data
        if user_token:
            parlays = [parlay for parlay in parlays if parlay.user_token == user_token]

        parlays_count = len(parlays)
        went_in_parlays_count = sum(1 for parlay in parlays if parlay.status == "WENT_IN")
        lost_parlays_count = sum(1 for parlay in parlays if parlay.status == "LOST")
        number_of_processors = sum(1 for parlay in parlays if parlay.status == "PENDING")
        winning_percentage = (went_in_parlays_count / parlays_count) * 100.0 if parlays_count > 0 else 0
        overall_win = sum(
            round(parlay.amount * parlay.coefficient * 0.01, 2) for parlay in parlays if parlay.status == "WENT_IN"
        )
        overall_loss = sum(round(parlay.amount * 0.01, 2) for parlay in parlays if parlay.status == "LOST")

        return {
            "parlays_count": parlays_count,
            "went_in_parlays_count": went_in_parlays_count,
            "lost_parlays_count": lost_parlays_count,
            "number_of_processors": number_of_processors,
            "winning_percentage": winning_percentage,
            "overall_win": overall_win,
            "overall_loss": overall_loss,
        }
