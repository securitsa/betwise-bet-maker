from enum import StrEnum
from typing import TypedDict

from domain.entities.parlay import ParlayStatus


class Ordering(StrEnum):
    DESC = "desc"
    ASC = "asc"


class ParlaySorting(StrEnum):
    BY_CREATION_DATE = "created_at"
    BY_STATUS_UPDATE_DATE = "status_updated_at"


class ParlayFilters(TypedDict):
    status: ParlayStatus
    user_token: str
