from enum import Enum


class KafkaTopics(str, Enum):
    USER_COMMANDS = "user_commands"
    OTRS_STATS = "otrs_stats"
    TG_BOT_MSGS = "tg_bot_messages"
    OTRS_NEW_TICKET = "otrs_new_ticket"
