import logging

from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError

from adapters.connection_engines.sql_alchemy.models import ParlaysORM
from adapters.repositories.parlay_repository.sqlalchemy_parlay_repository_mapper import SQLAlchemyParlayRepositoryMapper
from core.exceptions.external_exceptions import DatabaseException
from core.exceptions.parlay_exceptions import ParlayNotFoundException
from core.loggers import REPOSITORY_LOGGER
from domain.entities.parlay import Parlay
from domain.entities.parlay_statistics import ParlayStatistics
from ports.repositories.parlay_repository import ParlayRepository

logger = logging.getLogger(REPOSITORY_LOGGER)


class SQLAlchemyParlayRepository(ParlayRepository):
    def __init__(self, db):
        self.db = db
        self.mapper = SQLAlchemyParlayRepositoryMapper()

    async def save(self, parlay: Parlay) -> Parlay:
        try:
            query = select(ParlaysORM).where(ParlaysORM.token == parlay.token)
            result = await self.db.execute(query)
            if (parlay_orm := result.scalars().first()) is None:
                parlay_orm = ParlaysORM()
            await self.mapper.to_parlay_orm_entity(parlay_orm, parlay)
            self.db.add(parlay_orm)
            await self.db.flush()
            parlay.token = parlay_orm.token
            parlay.created_at = parlay_orm.created_at
            parlay.status_updated_at = parlay_orm.status_updated_at
            return parlay
        except SQLAlchemyError as e:
            logger.exception(e)
            await self.db.rollback()
            raise DatabaseException

    async def find_by_token(self, token: str) -> Parlay:
        try:
            query = select(ParlaysORM).where(ParlaysORM.token == token)
            result = await self.db.execute(query)
            if parlay_db := result.scalars().first():
                return self.mapper.to_parlay_entity(parlay_db)
            raise ParlayNotFoundException(token)
        except SQLAlchemyError as e:
            logger.exception(e)
            raise DatabaseException

    async def find_by_event_token(self, token: str) -> list[Parlay]:
        try:
            query = select(ParlaysORM).where(ParlaysORM.event_token == token)
            result = await self.db.execute(query)
            return [self.mapper.to_parlay_entity(parlay) for parlay in result.scalars().all()]
        except SQLAlchemyError as e:
            logger.exception(e)
            raise DatabaseException

    async def get_total_parlays_statistics(self) -> ParlayStatistics:
        statistics = await self.db.execute(text(self.__get_parlays_statistics_query()))
        return ParlayStatistics(**statistics.mappings().first() or {})

    async def get_user_parlays_statistics(self, user_token) -> ParlayStatistics:
        query = text(self.__get_parlays_statistics_query() + " WHERE user_token = :user_token")
        statistics = await self.db.execute(query, {"user_token": user_token})
        return ParlayStatistics(**statistics.mappings().first() or {})

    @staticmethod
    def __get_parlays_statistics_query():
        return """
            SELECT
                COUNT(*) AS parlays_count,
                SUM(CASE WHEN status = 'WENT_IN' THEN 1 ELSE 0 END) AS went_in_parlays_count,
                SUM(CASE WHEN status = 'LOST' THEN 1 ELSE 0 END) AS lost_parlays_count,
                SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) AS number_of_processors,
                (SUM(CASE WHEN status = 'WENT_IN' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS winning_percentage,
                SUM(CASE WHEN status = 'WENT_IN' THEN ROUND(CAST(amount * coefficient * 0.01 AS numeric), 2) ELSE 0 END) AS overall_win,
                SUM(CASE WHEN status = 'LOST' THEN ROUND(CAST(amount * 0.01 AS numeric), 2) ELSE 0 END) AS overall_loss
            FROM parlays
            """
