from enum import Enum


class UserCommand(Enum):
    START = "/start"
    HELP = "/help"
    SERVICE = "/service"
    CONTACTS = "/contacts"
    UNCLOSED = "/unclosed"
    TOTAL = "/total"
    RESULTS_BY_SHOP = "/results_by_shop"
    OTRS_STATS = "/otrs_stats"
    EQUIPMENT = "/equipment"
    OTRS_NEW_TICKET = "/otrs_new_ticket"
