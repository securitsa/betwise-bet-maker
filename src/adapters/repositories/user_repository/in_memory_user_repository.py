from domain.entities.parlay import LostParlay, Parlay, ParlaysHistory, ParlayStatus, WentInParlay


class InMemoryParlayRepository:
    def __init__(self):
        self.parlays_data: list[ParlaysHistory] = []

    def add_parlay(self, parlay: Parlay | WentInParlay | LostParlay):
        status = parlay.status
        if status == ParlayStatus.WENT_IN:
            self.parlays_data.append(ParlaysHistory(type=ParlayStatus.WENT_IN, item=parlay))
        elif status == ParlayStatus.LOST:
            self.parlays_data.append(ParlaysHistory(type=ParlayStatus.LOST, item=parlay))
        else:
            self.parlays_data.append(ParlaysHistory(type=ParlayStatus.PENDING, item=parlay))

    def get_parlays_history(
        self,
        user_token: str,
        page: int = 1,
        limit: int = 50,
        sort_by: ParlayStatus = ParlayStatus.PENDING,
    ) -> list[ParlaysHistory]:
        filtered_history = [
            history
            for history in self.parlays_data
            if history.type == sort_by and history.item.user_token == user_token
        ]
        offset = (page - 1) * limit
        return filtered_history[offset : offset + limit]

    def get_parlays_history_count(self, user_token: str, status: ParlayStatus = ParlayStatus.PENDING) -> int:
        return len(
            [
                history
                for history in self.parlays_data
                if history.type == status and history.item.user_token == user_token
            ]
        )
