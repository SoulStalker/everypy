from dataclasses import dataclass


@dataclass
class UnclosedShiftMessage:
    shop_number: int
    cashes: [int]
