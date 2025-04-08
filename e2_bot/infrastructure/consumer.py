import asyncio

from loguru import logger

from kafka import KafkaConsumer
import json
from e2_bot.app.ports.messaging import MessageReceiver


class KafkaMessageReceiver(MessageReceiver):
    def __init__(self, topic: str, bootstrap_servers: str, group_id: str):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8"))
        )

    async def consume(self, handler: callable):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._consume_blocking, handler)

    def _consume_blocking(self, handler: callable):
        logger.info("Kafka consumer started...")
        for message in self.consumer:
            logger.debug(f"Received message: {message.value}")
            handler(message.value)