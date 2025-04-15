from enum import Enum


class KafkaTopics(str, Enum):
    NOTIFICATIONS = "whatsapp_messages"
    USER_COMMANDS = "user_commands"
    OTRS_STATS = "otrs_stats"
    OTRS_NEW_TICKET = "otrs_new_ticket"
    TG_BOT_MSGS = "tg_bot_messages"
    EQUIPMENT = "equipment"
