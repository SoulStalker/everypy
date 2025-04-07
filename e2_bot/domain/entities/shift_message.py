from dataclasses import dataclass


@dataclass
class UnclosedShiftMessageEntity:
    shop_number: int
    cashes: [int]
