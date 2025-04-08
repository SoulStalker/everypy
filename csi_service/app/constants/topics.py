from enum import Enum


class KafkaTopics(str, Enum):
    USER_COMMANDS = "user_commands"
    TG_BOT_MSGS = "tg_bot_messages"
