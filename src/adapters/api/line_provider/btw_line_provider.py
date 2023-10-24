import logging

import aiohttp
import pydantic
from aiohttp.client_exceptions import ClientError

from adapters.api.line_provider.schema import EventItem, EventsCollection
from core.exceptions.external_exceptions import LineProviderException
from core.settings import BaseAppSettings
from domain.entities.event import Event
from ports.api.line_provider import LineProvider

logger = logging.getLogger()


class BTWLineProvider(LineProvider):
    def __init__(self, settings: BaseAppSettings):
        self.line_provider_api_url = settings.line_provider_api_url + "/v1/events?only_active=True"

    async def get_active_events(self) -> list[Event]:
        request_headers = {"Content-Type": "application/json"}
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.request("GET", self.line_provider_api_url, headers=request_headers)
                response_body = await response.json()
                try:
                    event_collection = EventsCollection.model_validate(response_body).items
                except pydantic.ValidationError as e:
                    logger.error(f"{self.__class__} - VALIDATION ERROR\n{e.__str__()}")
                    raise LineProviderException
                return [EventItem.to_entity(item) for item in event_collection]
        except ClientError as e:
            logger.exception(e)
            raise LineProviderException
