from enum import Enum


class UserCommand(Enum):
    START = "/start"
    HELP = "/help"
    SERVICE = "/service"
    CONTACTS = "/contacts"
    UNCLOSED = "/unclosed"
    TOTAL = "/total"
