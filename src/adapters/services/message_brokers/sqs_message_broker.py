import asyncio
import functools
import json
import signal
from typing import Callable, Coroutine, Iterable, NoReturn, Type

import pydantic
from aiobotocore.client import AioBaseClient
from aiobotocore.session import AioSession
from pydantic import BaseModel

from core.exceptions.consumer_exceptions import GracefulExitException
from core.exceptions.external_exceptions import MessageProducerException
from core.settings import BaseSettings, EnvironmentTypes
from message_consumers.dependencies.di_container import BaseContainer
from ports.services.message_broker import MessageBroker


class SQSMessageBroker(MessageBroker):
    queue_url: str
    dead_letter_queue_url: str

    def __init__(self, session: AioSession, settings: BaseSettings, logger, iterations: int | None = None):
        self.iterations = iterations
        self.session = session
        self.logger = logger
        self.client_config = {"region_name": "eu-west-3"}
        if settings.environment == EnvironmentTypes.local:
            self.client_config.update(settings.sqs_test_config)

        self.message_handlers_tasks: dict[str, asyncio.Task] = {}
        self.deletion_tasks: dict[str, asyncio.Task] = {}
        self.__configure_shutdown_events()
        self.attributes = {"senderService": {"StringValue": "Gamification Service", "DataType": "String"}}

    def __configure_shutdown_events(self):
        loop = asyncio.get_event_loop()
        for signame in ("SIGINT", "SIGTERM"):
            loop.add_signal_handler(getattr(signal, signame), self.__shutdown)

    def __shutdown(self) -> NoReturn:
        raise GracefulExitException

    async def pool(
        self,
        queue_name: str,
        message_handler: Callable[[Type[BaseModel] | dict, BaseContainer | None], Coroutine],
        dead_letter_queue_name: str | None = None,
        message_schema: Type[pydantic.BaseModel] | None = None,
        delete_on_exceptions: tuple[Type[Exception]] | None = None,
        graceful_shutdown_in_sec: int = 3,
        dead_letter_queue_threshold: int = 10,
        health_check_frequency_in_sec: int = 60,
        di_container: BaseContainer | None = None,
    ) -> None:
        async with self.session.create_client("sqs", **self.client_config) as client:
            await self.__get_queues_urls(client, queue_name, dead_letter_queue_name)
            if dead_letter_queue_name is not None:
                asyncio.create_task(self.__health_check(dead_letter_queue_threshold, health_check_frequency_in_sec))
            try:
                while True:
                    response = await self.__receive_message(client, queue_name)
                    for message in response.get("Messages", {}):
                        if not (message_body := self.__validate_message(message, message_schema)):
                            continue
                        self.logger.debug(
                            f"{self.__get_sender(message)} - Message {message['MessageId']} - IN PROGRESS"
                        )
                        task = asyncio.create_task(
                            self.__inject_dependencies(message_body, message_handler, di_container)
                        )
                        callback = functools.partial(
                            self.__message_handler_done_callback,
                            client=client,
                            message=message,
                            delete_on_exceptions=delete_on_exceptions,
                        )
                        task.add_done_callback(callback)
                        self.message_handlers_tasks[message["MessageId"]] = task
                    if self.iterations is not None:
                        self.iterations -= 1
                        if self.iterations < 0:
                            break
            except GracefulExitException:
                await self.__close_pending_tasks(graceful_shutdown_in_sec, self.message_handlers_tasks.values())
                await self.__close_pending_tasks(graceful_shutdown_in_sec, self.deletion_tasks.values())

    async def __get_queues_urls(self, client: AioBaseClient, queue_name: str, dead_letter_queue_name: str | None):
        if not hasattr(self, "queue_url"):
            self.queue_url = (await client.get_queue_url(QueueName=queue_name))["QueueUrl"]
        if not hasattr(self, "dead_letter_queue_url") and dead_letter_queue_name is not None:
            self.dead_letter_queue_url = (await client.get_queue_url(QueueName=dead_letter_queue_name))["QueueUrl"]

    async def __health_check(self, dead_letter_queue_threshold: int, health_check_frequency_in_sec: int):
        async with self.session.create_client("sqs", **self.client_config) as client:
            try:
                while True:
                    response = await client.get_queue_attributes(
                        QueueUrl=self.dead_letter_queue_url, AttributeNames=["All"]
                    )
                    msg_count = int(response["Attributes"]["ApproximateNumberOfMessages"])
                    if msg_count >= dead_letter_queue_threshold:
                        self.logger.warning(f"HEALTH CHECK - Dead letter queue contains {msg_count} messages")
                    await asyncio.sleep(health_check_frequency_in_sec)
            except:
                self.logger.exception(f"HEALTH CHECK - Not able to send a request")

    async def __receive_message(self, client: AioBaseClient, queue_name: str):
        try:
            return await client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=5,
                WaitTimeSeconds=5,
                AttributeNames=["All"],
                MessageAttributeNames=["All"],
            )
        except:
            self.logger.critical(f"Not able to receive messages from {queue_name} queue")
            await asyncio.sleep(10)
            return {}

    def __validate_message(self, message: dict, message_schema: Type[pydantic.BaseModel] | None):
        if message_schema is not None:
            try:
                return message_schema.parse_raw(message["Body"])
            except pydantic.ValidationError as e:
                self.logger.error(
                    f"{self.__get_sender(message)} - Message {message['MessageId']} - VALIDATION ERROR\n{e.__str__()}"
                )
        else:
            return message["Body"]

    @staticmethod
    async def __inject_dependencies(
        message_body: pydantic.BaseModel | dict,
        message_handler: Callable[[Type[BaseModel] | dict, BaseContainer | None], Coroutine],
        di_container: Type[BaseContainer] | None = None,
    ):
        if di_container:
            async with di_container() as container:
                await message_handler(message_body, container)
        else:
            await message_handler(message_body, None)

    def __message_handler_done_callback(
        self, task: asyncio.Task, client: AioBaseClient, message: dict, delete_on_exceptions: set[Exception] | None
    ):
        del self.message_handlers_tasks[message["MessageId"]]
        sender = self.__get_sender(message)
        if (exc := task.exception()) is None:
            self.logger.info(f"{sender} - Message {message['MessageId']} - SUCCESS")
            self.deletion_tasks[message["MessageId"]] = asyncio.create_task(self.__delete_message(client, message))
        elif delete_on_exceptions is not None and type(task.exception()) in delete_on_exceptions:
            self.logger.error(f"{sender} - Message {message['MessageId']} - PROCESSING ERROR", exc_info=exc)
            self.deletion_tasks[message["MessageId"]] = asyncio.create_task(self.__delete_message(client, message))
        else:
            self.logger.error(f"{sender} - Message {message['MessageId']} - PROCESSING ERROR", exc_info=exc)

    async def __delete_message(self, client: AioBaseClient, message: dict):
        try:
            await client.delete_message(QueueUrl=self.queue_url, ReceiptHandle=message["ReceiptHandle"])
            del self.deletion_tasks[message["MessageId"]]
            self.logger.debug(f"{self.__get_sender(message)} - Message {message['MessageId']} - DELETED")
        except:
            self.logger.exception(f"{self.__get_sender(message)} - Message {message['MessageId']} - DELETION ERROR")

    @staticmethod
    async def __close_pending_tasks(graceful_shutdown_in_sec: int, tasks: Iterable[asyncio.Task]):
        waiters = [asyncio.wait_for(task, graceful_shutdown_in_sec) for task in tasks]
        for task in waiters:
            try:
                await task
            except asyncio.exceptions.TimeoutError:
                pass

    @staticmethod
    def __get_sender(message: dict) -> str:
        return message.get("MessageAttributes", {}).get("senderService", {}).get("StringValue")

    async def send_message(self, queue_name: str, payload: dict) -> str:
        sender = self.attributes.get("senderService", {}).get("StringValue")
        async with self.session.create_client("sqs", **self.client_config) as client:
            try:
                queue_url = (await client.get_queue_url(QueueName=queue_name))["QueueUrl"]
                message = await client.send_message(
                    QueueUrl=queue_url,
                    MessageBody=json.dumps(payload),
                    MessageAttributes=self.attributes,
                    DelaySeconds=1,
                )
                self.logger.info(f"{sender} - Message {message['MessageId']} - SENT")
                return message["MessageId"]
            except Exception as e:
                self.logger.exception(f"{sender} - Message {message['MessageId']} - SENDING ERROR")
                raise MessageProducerException

    async def purge_all(self, queue_name: str) -> None:
        async with self.session.create_client("sqs", **self.client_config) as client:
            queue_url = (await client.get_queue_url(QueueName=queue_name))["QueueUrl"]
            try:
                await client.purge_queue(QueueUrl=queue_url)
            except:
                pass
