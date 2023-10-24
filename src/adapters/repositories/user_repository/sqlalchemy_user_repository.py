import logging
from typing import Unpack

from sqlalchemy import desc, func, select
from sqlalchemy.exc import SQLAlchemyError

from adapters.connection_engines.sql_alchemy.models import ParlaysORM
from adapters.repositories.user_repository.sqlalchemy_user_repository_mapper import SQLAlchemyUserRepositoryMapper
from core.exceptions.external_exceptions import DatabaseException
from core.loggers import REPOSITORY_LOGGER
from domain.entities.parlay import ParlaysHistory
from ports.repositories.user_repository import UserRepository
from usecases.enum_models import Ordering, ParlayFilters, ParlaySorting

logger = logging.getLogger(REPOSITORY_LOGGER)


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db):
        self.db = db
        self.mapper = SQLAlchemyUserRepositoryMapper()

    async def get_parlays_history(
        self,
        page: int = 1,
        limit: int = 50,
        sort_by: ParlaySorting = ParlaySorting.BY_CREATION_DATE,
        order_by: Ordering = Ordering.ASC,
        **filters: Unpack[ParlayFilters],
    ) -> list[ParlaysHistory]:
        offset = (page - 1) * limit
        filter_expressions = self.__get_filter_expression(ParlaysORM, filters)
        order_expression = self.__get_order_expression(order_by, sort_by)
        try:
            query = select(ParlaysORM).where(*filter_expressions).offset(offset).limit(limit).order_by(order_expression)
            result = await self.db.execute(query)
            return self.mapper.to_coins_history_events(result.scalars().all(), filters.get("user_token"))
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseException

    async def get_parlays_history_count(self, **filters: Unpack[ParlayFilters]) -> int:
        filter_expressions = self.__get_filter_expression(ParlaysORM, filters)
        try:
            query = select(func.count("*")).select_from(ParlaysORM).where(*filter_expressions)
            result = await self.db.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseException

    @staticmethod
    def __get_filter_expression(model, filters: Unpack[ParlayFilters]):
        return [getattr(model, field) == value for field, value in filters.items() if value is not None]

    @staticmethod
    def __get_order_expression(order_by: Ordering, sort_by: ParlaySorting):
        return desc(getattr(ParlaysORM, sort_by)) if order_by == Ordering.DESC else getattr(ParlaysORM, sort_by)
