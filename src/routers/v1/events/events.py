from fastapi import APIRouter, Depends

from routers.dependencies.usecases import get_list_events_caching_use_case
from routers.v1.events.schema import EventItem, EventsCollection
from usecases.events.list_events_caching_use_case import ListEventsCachingUseCase

router = APIRouter(prefix="/v1")


@router.get("/events", response_model=EventsCollection)
async def list_events(
    list_events_use_case: ListEventsCachingUseCase = Depends(get_list_events_caching_use_case),
):
    events = await list_events_use_case()
    return EventsCollection(items=[EventItem.from_entity(event) for event in events], total_count=len(events))
