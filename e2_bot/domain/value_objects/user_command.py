from enum import Enum


class UserCommand(Enum):
    START = "/start"
    HELP = "/help"
    SERVICE = "/service"
    CONTACTS = "/contacts"
    UNCLOSED = "/unclosed"
    TOTAL = "/total"
    RESULTS_BY_SHOP = "/results_by_shop"
