from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from domain.entities.parlay import ParlayStatus


class Base(DeclarativeBase):
    type_annotation_map = {datetime: sa.DateTime(timezone=True)}


class ParlaysORM(Base):
    __tablename__ = "parlays"
    __table_args__ = (sa.Index("events_user_token_created_at_idx", "user_token", "created_at", unique=False),)

    token: Mapped[UUID] = mapped_column(primary_key=True, server_default=sa.text("gen_random_uuid()"))
    user_token: Mapped[str]
    event_token: Mapped[str]
    amount: Mapped[str]
    coefficient: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=sa.func.now())
    status: Mapped[ParlayStatus]
    status_updated_at: Mapped[datetime | None]
