from pydantic import BaseModel

from domain.entities.parlay_statistics import ParlayStatistics


class ParlayStatisticsItem(BaseModel):
    parlays_count: int
    went_in_parlays_count: int
    lost_parlays_count: int
    number_of_processors: int
    winning_percentage: float
    overall_win: float
    overall_loss: float

    @classmethod
    def from_entity(cls, item: ParlayStatistics):
        return cls(
            parlays_count=item.parlays_count,
            went_in_parlays_count=item.went_in_parlays_count,
            lost_parlays_count=item.lost_parlays_count,
            number_of_processors=item.number_of_processors,
            winning_percentage=item.winning_percentage,
            overall_win=item.overall_win,
            overall_loss=item.overall_loss,
        )
