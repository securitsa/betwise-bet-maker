from dataclasses import dataclass


@dataclass
class ParlayStatistics:
    parlays_count: int = 0
    went_in_parlays_count: int | None = None
    lost_parlays_count: int | None = None
    number_of_processors: int | None = None
    winning_percentage: float | None = None
    overall_win: float | None = None
    overall_loss: float | None = None
