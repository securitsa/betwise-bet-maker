import logging
from typing import Unpack

from sqlalchemy import desc, func, select
from sqlalchemy.exc import SQLAlchemyError

from adapters.connection_engines.sql_alchemy.models import ParlaysORM
from adapters.repositories.parlay_repository.sqlalchemy_parlay_repository_mapper import SQLAlchemyParlayRepositoryMapper
from core.exceptions.external_exceptions import DatabaseException
from core.exceptions.parlay_exceptions import ParlayNotFoundException
from core.loggers import REPOSITORY_LOGGER
from domain.entities.parlay import Parlay
from ports.repositories.parlay_repository import ParlayRepository
from usecases.enum_models import Ordering, ParlayFilters, ParlaySorting

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

    async def exists(self, token: str) -> bool:
        try:
            result = await self.db.execute(select(1).where(ParlaysORM.token == token))
            return result.scalars().first() is not None
        except SQLAlchemyError as e:
            logger.exception(e)
            await self.db.rollback()
            raise DatabaseException

    async def list(
        self,
        page: int = 1,
        limit: int = 50,
        sort_by: ParlaySorting = ParlaySorting.BY_CREATION_DATE,
        order_by: Ordering = Ordering.ASC,
        **filters: Unpack[ParlayFilters],
    ) -> list[Parlay]:
        offset = (page - 1) * limit
        filter_expressions = self.__get_filter_expression(ParlaysORM, filters)
        order_expression = self.__get_order_expression(order_by, sort_by)
        try:
            query = select(ParlaysORM).where(*filter_expressions).offset(offset).limit(limit).order_by(order_expression)
            result = await self.db.execute(query)
            return [self.mapper.to_parlay_entity(parlay) for parlay in result.scalars().all()]
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseException

    async def count(self, **filters: Unpack[ParlayFilters]) -> int:
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
