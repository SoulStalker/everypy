from enum import Enum


class KafkaTopics(str, Enum):
    USER_COMMANDS = "user_commands"
    EQUIPMENT = "equipment"
    TG_BOT_MSGS = "tg_bot_messages"
