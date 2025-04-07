from enum import Enum


class Command(Enum):
    START = "/start"
    HELP = "/help"
    SETTINGS = "/settings"
    UNCLOSED = "/unclosed"
