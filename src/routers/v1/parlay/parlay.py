from fastapi import APIRouter, Depends

from domain.value_objects.user import User
from routers.dependencies.security import admin_user_authorizer, get_user_from_access_token
from routers.dependencies.usecases import get_save_parlay_use_case
from routers.v1.parlay.schema import ParlayInput, ParlayItem
from usecases.parlays.save_parlay_use_case import SaveParlayUseCase

router = APIRouter(prefix="/v1")


@router.post("/parlay", response_model=ParlayItem, dependencies=[Depends(admin_user_authorizer)])
async def post_parlay(
    parlay: ParlayInput,
    user: User = Depends(get_user_from_access_token),
    save_parlay_usecase: SaveParlayUseCase = Depends(get_save_parlay_use_case),
):
    parlay = await save_parlay_usecase(parlay.to_entity(user.token))
    return ParlayItem.from_entity(parlay)
