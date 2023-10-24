from fastapi import APIRouter, Depends

from domain.value_objects.user import User
from ports.repositories.parlay_repository import ParlayRepository
from routers.dependencies.repositories import get_parlay_repository
from routers.dependencies.security import admin_authorizer, admin_user_authorizer, get_user_from_access_token
from routers.v1.me.schema import ParlayStatisticsItem

router = APIRouter(prefix="/v1")


@router.get("/me/statistics", response_model=ParlayStatisticsItem, dependencies=[Depends(admin_user_authorizer)])
async def get_parlays_statistics(
    parlay_repository: ParlayRepository = Depends(get_parlay_repository),
    user: User = Depends(get_user_from_access_token),
):
    statistics = await parlay_repository.get_user_parlays_statistics(user.token)
    return ParlayStatisticsItem.from_entity(statistics)


@router.get("/app/statistics", response_model=ParlayStatisticsItem, dependencies=[Depends(admin_authorizer)])
async def get_parlays_statistics(
    parlay_repository: ParlayRepository = Depends(get_parlay_repository),
):
    statistics = await parlay_repository.get_total_parlays_statistics()
    return ParlayStatisticsItem.from_entity(statistics)
