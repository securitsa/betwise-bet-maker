from dataclasses import dataclass


@dataclass
class ParlayStatistics:
    parlays_count: int
    went_in_parlays_count: int
    lost_parlays_count: int
    number_of_processors: int
    winning_percentage: float
    overall_win: float
    overall_loss: float
