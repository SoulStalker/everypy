import json

from kafka import KafkaProducer
from loguru import logger

from gsheet_service.configs import load_config

config = load_config('.env')

producer = KafkaProducer(bootstrap_servers=config.kafka.broker, value_serializer=lambda v: json.dumps(v).encode("utf-8"))


def send_message(topic: str, message: dict):
    logger.debug(f"Sending message to topic {topic}")
    producer.send(topic, message)
    producer.flush()
