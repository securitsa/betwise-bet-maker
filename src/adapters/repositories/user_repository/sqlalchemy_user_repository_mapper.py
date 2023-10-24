from adapters.connection_engines.sql_alchemy.models import ParlaysORM
from domain.entities.parlay import LostParlay, Parlay, ParlaysHistory, ParlayStatus, WentInParlay


class SQLAlchemyUserRepositoryMapper:
    @staticmethod
    def to_coins_history_events(raw_events: list[ParlaysORM], user_token: str) -> list[ParlaysHistory]:
        events = []
        for raw_event in raw_events:
            event_type = raw_event.status
            if event_type == ParlayStatus.WENT_IN:
                event = WentInParlay(
                    token=raw_event.token,
                    event_token=raw_event.event_token,
                    winnings=round(raw_event.amount * raw_event.coefficient * 0.01, 2),
                    status=raw_event.status,
                    created_at=raw_event.created_at,
                    user_token=user_token,
                )
            elif event_type == ParlayStatus.LOST:
                event = LostParlay(
                    token=raw_event.token,
                    event_token=raw_event.event_token,
                    loss=round(raw_event.amount * 0.01, 2),
                    status=raw_event.status,
                    created_at=raw_event.created_at,
                    user_token=user_token,
                )
            else:
                event = Parlay(
                    token=raw_event.token,
                    event_token=raw_event.event_token,
                    amount=raw_event.amount,
                    status=raw_event.status,
                    coefficient=raw_event.coefficient,
                    created_at=raw_event.created_at,
                    status_updated_at=raw_event.status_updated_at,
                    user_token=user_token,
                )
            events.append(ParlaysHistory(type=event_type, item=event))
        return events
