import asyncio

from loguru import logger

from otrs_service.app.constants import KafkaTopics
from otrs_service.configs import load_config
from otrs_service.infrastructure.consumer import start_consumer
from otrs_service.infrastructure.producer import send_message
from otrs_service.service.service import get_stats

config = load_config('.env')


async def process_message(msg):
    logger.info(f"Обработка сообщения: {msg}")
    if msg["command"] == KafkaTopics.OTRS_STATS.name:
        stats, finish = await get_stats()
        send_message(KafkaTopics.TG_BOT_MSGS.value, {"command": KafkaTopics.OTRS_STATS.name, "content": stats})
        send_message(KafkaTopics.TG_BOT_MSGS.value, {"command": KafkaTopics.OTRS_STATS.name, "content": finish})
    else:
        send_message(KafkaTopics.TG_BOT_MSGS.value, {"command": KafkaTopics.OTRS_STATS.name, "content": "Invalid command"})


async def main():
    logger.info("Запуск слушателя Kafka...")
    for msg in start_consumer(config.kafka.broker, "csi_service"):
        logger.debug(f"Получено сообщение: {msg}")
        await process_message(msg)


if __name__ == "__main__":
    asyncio.run(main())
