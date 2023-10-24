import asyncio
import logging.config
from pathlib import Path

from adapters.services.message_brokers.session import session
from adapters.services.message_brokers.sqs_message_broker import SQSMessageBroker
from core.config import settings
from core.loggers import CONSUMER_LOGGER
from message_consumers.event_statuses.di_container import EventStatusContainer
from message_consumers.event_statuses.schema import EventStatusItem
from message_consumers.sqs_consumer.base_consumer import BaseConsumer


class FriendRewardConsumer(BaseConsumer):
    queue_name = settings.events_queue
    dead_letter_queue_name = settings.events_dead_letter_queue
    message_schema = EventStatusItem
    di_container = EventStatusContainer

    async def message_handler(self, message: EventStatusItem, container: EventStatusContainer) -> None:
        await container.update_parlay_status_usecase(EventStatusItem.to_entity(message))


if __name__ == "__main__":
    logging.config.fileConfig(Path(__file__).parent.parent.parent / "logging.conf", disable_existing_loggers=False)
    for log in ("botocore", "aiobotocore"):
        logging.getLogger(log).setLevel(logging.ERROR)
    logger = logging.getLogger(CONSUMER_LOGGER)
    message_broker = SQSMessageBroker(session, settings, logger)
    consumer = FriendRewardConsumer(message_broker)
    asyncio.run(consumer.start())
