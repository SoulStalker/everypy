import asyncio
import json

from kafka import KafkaConsumer
from loguru import logger

from e2_bot.app.ports.messaging import MessageReceiver


class KafkaMessageReceiver(MessageReceiver):
    def __init__(self, topic: str, bootstrap_servers: str, group_id: str):
        self.topic = topic
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=kafka_deserializer  # Используем новую функцию
        )

    async def consume(self, handler: callable):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._consume_blocking, handler)

    def _consume_blocking(self, handler: callable):
        logger.info(f"Kafka consumer started listening to topic '{self.topic}'...")
        for message in self.consumer:
            logger.debug(f"Received message from topic '{self.topic}'")
            if message.value is not None:  # Дополнительная проверка
                handler(message.value)
            else:
                logger.warning("Skipped None message")


def kafka_deserializer(v):
    if v is None:
        logger.warning("Received message with None value")
        return None
    try:
        return json.loads(v.decode("utf-8"))
    except Exception as e:
        logger.error(f"Deserialization error: {str(e)}", exc_info=True)
        return None
