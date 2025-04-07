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

    def consume(self, handler: callable) -> None:
        for message in self.consumer:
            handler(message.value)
