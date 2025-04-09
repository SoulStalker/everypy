import json
from kafka import KafkaConsumer
from csi_service.app.constants import KafkaTopics

from loguru import logger


def start_consumer(bootstrap_servers: str, group_id: str):
    consumer = KafkaConsumer(
        KafkaTopics.USER_COMMANDS.value,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logger.debug(f"Kafka consumer started listening to topic '{KafkaTopics.USER_COMMANDS.value}'...")
    for message in consumer:
        yield message.value
