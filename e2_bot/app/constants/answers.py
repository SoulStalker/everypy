from enum import Enum


class TgAnswer(str, Enum):
    GOOD_BOY = "good_boy"
    BAD_BOY = "bad_boy"
    ALL_CLOSED = "all_closed"
    YES_SIR = "yes_sir"
