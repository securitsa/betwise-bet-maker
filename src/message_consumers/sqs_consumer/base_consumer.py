import logging
from abc import ABC, abstractmethod
from typing import Type

import pydantic

from core.loggers import CONSUMER_LOGGER
from message_consumers.dependencies.di_container import BaseContainer
from ports.services.message_broker import MessageBroker

logger = logging.getLogger(CONSUMER_LOGGER)


class BaseConsumer(ABC):
    """
    A base class for SQS consumers. In a child class `queue_name` should be defined
    to receive messages from the queue.
    Other attributes:
        - `dead_letter_queue_name` (optional) - can be specified to perform
           a health check on the dead letter queue if one is configured;
        - `health_check_frequency_in_sec` (default: 60) - frequency of the
           heath check requests;
        - `graceful_shutdown_in_sec` (default: 3) - time in seconds for the pending message
           handler tasks to finish after either SIGINT or SIGTERM is triggered;
        - `dead_letter_queue_threshold` (default: 10) - the warning message is logged in case
           the number of the messages in the dead letter queue is higher than the threshold;
        - `message_schema` (optional) - pydantic model to serialize and validate
           the message from the queue. If specified, the model instance will be passed
           to the message handler in case of successful data serialization and validation;
        - `delete_on_exceptions` (optional) - in occurrence of the specified exceptions
           the message will be deleted from the queue.
    """

    queue_name: str
    dead_letter_queue_name: str | None = None
    health_check_frequency_in_sec: int = 60
    graceful_shutdown_in_sec: int = 3
    dead_letter_queue_threshold: int = 10
    message_schema: Type[pydantic.BaseModel] | None = None
    delete_on_exceptions: set[Exception] | None = None
    di_container: BaseContainer | None = None

    def __init__(self, message_broker: MessageBroker):
        self.message_broker = message_broker
        if not hasattr(self, "queue_name"):
            raise ValueError(f"Please define queue name for {self.__class__.__name__}")

    async def start(self) -> None:
        await self.message_broker.pool(
            self.queue_name,
            self.message_handler,
            self.dead_letter_queue_name,
            self.message_schema,
            self.delete_on_exceptions,
            self.graceful_shutdown_in_sec,
            self.dead_letter_queue_threshold,
            self.health_check_frequency_in_sec,
            self.di_container,
        )

    @abstractmethod
    async def message_handler(self, message: Type[pydantic.BaseModel], container: BaseContainer) -> None:
        raise NotImplementedError
