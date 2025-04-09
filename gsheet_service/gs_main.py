import asyncio

from loguru import logger

from app.constants.topics import KafkaTopics
from gsheet_service.configs import load_config
from gsheet_service.infrastructure import start_consumer
from gsheet_service.service import get_data
from infrastructure.producer import send_message

config = load_config()


def send_gs_info(command: str):
    content = get_data()
    topic = KafkaTopics.TG_BOT_MSGS.value
    payload = {"command": command, "content": content}
    send_message(topic, payload)


async def process_message(msg):
    logger.info(f"Обработка сообщения: {msg}")
    if msg["command"] in KafkaTopics.EQUIPMENT.name:
        send_gs_info(KafkaTopics.EQUIPMENT.name)
    else:
        send_message(KafkaTopics.TG_BOT_MSGS.name, {"command": KafkaTopics.EQUIPMENT.name, "content": "Invalid command"})


async def main():
    logger.info("Запуск слушателя Kafka...")
    for msg in start_consumer(config.kafka.broker, "csi_service"):
        logger.debug(f"Получено сообщение: {msg}")

        await process_message(msg)


if __name__ == "__main__":
    asyncio.run(main())
