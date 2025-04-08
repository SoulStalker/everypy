from enum import Enum


class KafkaTopics(str, Enum):
    USER_COMMANDS = "user_commands"
    OTRS_NOTIFICATIONS = "otrs_notifications"
