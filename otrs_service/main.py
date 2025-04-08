import asyncio

from loguru import logger

from otrs_service.infrastructure.consumer import start_consumer
from otrs_service.infrastructure.producer import send_message
from otrs_service.service.service import get_message, get_stats
from otrs_service.app.constants import KafkaTopics

from otrs_service.configs import load_config

config = load_config('.env')


async def process_message(msg):
    logger.info(f"Обработка сообщения: {msg}")
    await get_message(msg)
    stats, finish = await get_stats()

    send_message(KafkaTopics.TG_BOT_MSGS.value, {"command": "OTRS_STATS", "content": stats})
    send_message(KafkaTopics.TG_BOT_MSGS.value, {"command": "OTRS_STATS", "content": finish})


async def main():
    logger.info("Запуск слушателя Kafka...")
    for msg in start_consumer(config.kafka.broker, "csi_service"):
        logger.debug(f"Получено сообщение: {msg}")
        await process_message(msg)


if __name__ == "__main__":
    asyncio.run(main())
