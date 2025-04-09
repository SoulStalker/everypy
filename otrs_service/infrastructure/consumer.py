import json
from kafka import KafkaConsumer
from loguru import logger

from otrs_service.app.constants import KafkaTopics


def start_consumer(bootstrap_servers: str, group_id: str):
    consumer = KafkaConsumer(
        KafkaTopics.OTRS_STATS.value,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logger.debug(f"Kafka consumer started listening to topic '{KafkaTopics.OTRS_STATS.value}'...")
    for message in consumer:
        yield message.value
