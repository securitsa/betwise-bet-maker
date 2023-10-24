from fastapi import APIRouter, Depends, Request

from domain.entities.parlay import ParlayStatus
from domain.value_objects.user import User
from routers.dependencies.security import admin_user_authorizer, get_user_from_access_token
from routers.dependencies.usecases import get_list_user_parlay_history_use_case
from routers.hateoas import HateoasModel
from routers.v1.parlays.schema import ParlayHistoryCollection, ParlayHistoryItem
from usecases.enum_models import Ordering, ParlaySorting
from usecases.users.list_user_parlay_history_use_case import ListUserParlayHistoryUseCase

router = APIRouter(prefix="/v1")


@router.get("/parlays", response_model=ParlayHistoryCollection, dependencies=[Depends(admin_user_authorizer)])
async def get_parlays_history(
    request: Request,
    page: int = 1,
    limit: int = 50,
    sort_by: ParlaySorting = ParlaySorting.BY_CREATION_DATE.value,
    order_by: Ordering = Ordering.ASC.value,
    status_filter: ParlayStatus = None,
    list_parlays_use_case: ListUserParlayHistoryUseCase = Depends(get_list_user_parlay_history_use_case),
    user: User = Depends(get_user_from_access_token),
):
    events, count = await list_parlays_use_case(
        page, limit, sort_by, order_by, status=status_filter, user_token=user.token
    )
    return HateoasModel(
        items=[ParlayHistoryItem.from_entity(event) for event in events],
        limit=limit,
        page=page,
        total_count=count,
        path=request.url.path,
    )
