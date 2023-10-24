import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from adapters.connection_engines.sql_alchemy.models import ParlaysORM
from adapters.repositories.parlay_repository.sqlalchemy_parlay_repository_mapper import SQLAlchemyParlayRepositoryMapper
from core.exceptions.external_exceptions import DatabaseException
from core.exceptions.parlay_exceptions import ParlayNotFoundException
from core.loggers import REPOSITORY_LOGGER
from domain.entities.parlay import Parlay
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

    async def exists(self, token: str) -> bool:
        try:
            result = await self.db.execute(select(1).where(ParlaysORM.token == token))
            return result.scalars().first() is not None
        except SQLAlchemyError as e:
            logger.exception(e)
            await self.db.rollback()
            raise DatabaseException

    async def find_by_event_token(self, token: str) -> list[Parlay]:
        try:
            query = select(ParlaysORM).where(ParlaysORM.event_token == token)
            result = await self.db.execute(query)
            return [self.mapper.to_parlay_entity(parlay) for parlay in result.scalars().all()]
        except SQLAlchemyError as e:
            logger.exception(e)
            raise DatabaseException
