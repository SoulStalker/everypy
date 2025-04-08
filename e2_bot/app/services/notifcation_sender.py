from e2_bot.app.constants import KafkaTopics
from e2_bot.domain.value_objects import UserCommand
from e2_bot.infrastructure import KafkaMessageSender
from e2_bot.configs import load_config

config = load_config('.env')

producer = KafkaMessageSender(config.kafka.broker)


def send_otrs_notifications():
    payload = {"chat_id": config.tg_bot.chat_id, "command": UserCommand.OTRS_STATS.name}
    producer.send(KafkaTopics.OTRS_STATS.value, payload)
