from abc import ABC, abstractmethod
from asyncio import Task
from typing import Callable, Coroutine, Type

import pydantic
from pydantic import BaseModel

from message_consumers.dependencies.di_container import BaseContainer


class MessageBroker(ABC):
    message_handlers_tasks: dict[str, Task]
    queues: dict[str, str]

    @abstractmethod
    async def pool(
        self,
        queue_name: str,
        message_handler: Callable[[Type[BaseModel] | dict], Coroutine],
        dead_letter_queue_name: str | None,
        message_schema: Type[pydantic.BaseModel],
        delete_on_exceptions: set[Exception],
        graceful_shutdown_in_sec: int = 3,
        dead_letter_queue_threshold: int = 10,
        health_check_frequency_in_sec: int = 60,
        di_container: BaseContainer = None,
    ) -> None:
        pass
