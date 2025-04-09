from enum import Enum


class KafkaTopics(str, Enum):
    NOTIFICATIONS = "whatsapp_messages"
    USER_COMMANDS = "user_commands"
    OTRS_STATS = "otrs_stats"
    TG_BOT_MSGS = "tg_bot_messages"
    EQUIPMENT = "equipment"
