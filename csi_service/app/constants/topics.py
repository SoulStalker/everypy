from enum import Enum


class KafkaTopics(str, Enum):
    CSI_RESPONSES = "csi_responses"
    USER_COMMANDS = "user_commands"
