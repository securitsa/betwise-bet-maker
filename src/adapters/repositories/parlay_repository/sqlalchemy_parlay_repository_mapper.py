from adapters.connection_engines.sql_alchemy import models
from domain.entities.parlay import Parlay


class SQLAlchemyParlayRepositoryMapper:
    @staticmethod
    def to_parlay_entity(parlay_orm: models.ParlaysORM) -> Parlay:
        return Parlay(
            token=parlay_orm.token,
            user_token=parlay_orm.user_token,
            event_token=parlay_orm.event_token,
            amount=parlay_orm.amount,
            coefficient=parlay_orm.coefficient,
            status=parlay_orm.status,
            created_at=parlay_orm.created_at,
            status_updated_at=parlay_orm.status_updated_at,
        )

    @staticmethod
    async def to_parlay_orm_entity(parlay_orm: models.ParlaysORM, parlay: Parlay) -> None:
        parlay_orm.token = parlay.token
        parlay_orm.user_token = parlay.user_token
        parlay_orm.event_token = parlay.event_token
        parlay_orm.amount = parlay.amount
        parlay_orm.coefficient = parlay.coefficient
        parlay_orm.status = parlay.status
