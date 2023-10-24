from fastapi import Depends

from routers.dependencies.api import get_line_provider_api
from routers.dependencies.repositories import get_event_caching_repository, get_parlay_repository
from usecases.events.list_events_caching_use_case import ListEventsCachingUseCase
from usecases.parlays.save_parlay_use_case import SaveParlayUseCase


def get_save_parlay_use_case(
    parlay_repository=Depends(get_parlay_repository),
    line_provider=Depends(get_line_provider_api),
    event_caching_repository=Depends(get_event_caching_repository),
):
    return SaveParlayUseCase(parlay_repository, line_provider, event_caching_repository)


def get_list_events_caching_use_case(
    line_provider=Depends(get_line_provider_api),
    event_caching_repository=Depends(get_event_caching_repository),
):
    return ListEventsCachingUseCase(line_provider, event_caching_repository)
