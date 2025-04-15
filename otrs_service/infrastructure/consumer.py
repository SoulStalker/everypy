# import json
#
# from loguru import logger
#
# from otrs_service.app.constants import KafkaTopics
#
#
# def start_consumer(bootstrap_servers: str, group_id: str):
#     consumer = KafkaConsumer(
#         KafkaTopics.OTRS_STATS.value,
#         bootstrap_servers=bootstrap_servers,
#         group_id=group_id,
#         value_deserializer=lambda m: json.loads(m.decode('utf-8'))
#     )
#     logger.debug(f"Kafka consumer started listening to topic '{KafkaTopics.OTRS_STATS.value}'...")
#     for message in consumer:
#         yield message.value
import json

from aiokafka import AIOKafkaConsumer
from loguru import logger

from otrs_service.app.constants import KafkaTopics
from otrs_service.service.service import process_message


async def consume(bootstrap_servers: str, group_id: str):
    consumer = AIOKafkaConsumer(
        KafkaTopics.OTRS_STATS.value,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        session_timeout_ms=30000,  # 30 секунд
        heartbeat_interval_ms=10000,  # 10 секунд
        max_poll_interval_ms=600000,  # 10 минут
        max_poll_records=10,
        auto_offset_reset='earliest',
    )
    await consumer.start()
    try:
        async for msg in consumer:
            logger.debug(f"Kafka consumer started listening to topic '{KafkaTopics.OTRS_STATS.value}'...")
            await process_message(msg.value)
    finally:
        await consumer.stop()
