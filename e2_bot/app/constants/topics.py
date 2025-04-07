from enum import Enum


class KafkaTopics(str, Enum):
    NOTIFICATIONS = "whatsapp_messages"
    CSI_RESPONSES = "csi_responses"
    USER_COMMANDS = "user_commands"
