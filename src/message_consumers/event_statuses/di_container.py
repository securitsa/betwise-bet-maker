from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repositories.parlay_repository.sqlalchemy_parlay_repository import SQLAlchemyParlayRepository
from message_consumers.dependencies.di_container import BaseContainer
from usecases.parlays.update_parlay_status_use_case import UpdateParlayStatusUseCase


class EventStatusContainer(BaseContainer):
    def init_dependencies(self, db_session: AsyncSession) -> None:
        self.parlay_repository = SQLAlchemyParlayRepository(db_session)
        self.update_parlay_status_usecase = UpdateParlayStatusUseCase(self.parlay_repository)
