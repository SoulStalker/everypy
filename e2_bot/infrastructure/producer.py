from kafka import KafkaProducer
import json
from e2_bot.app.ports.messaging import MessageSender


class KafkaMessageSender(MessageSender):
    def __init__(self, bootstrap_servers: str):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def send(self, topic: str, message: dict) -> None:
        self.producer.send(topic, message)
