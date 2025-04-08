import datetime
from dataclasses import dataclass

from e2_bot.domain.entities import ShopEntity


@dataclass
class USMessageEntity:
    shop_number: int
    cashes: [int]

    def format(self, shop: ShopEntity):
        cashes = ", ".join(map(str, self.cashes))
        if len(self.cashes) == 1:
            formated_msg = f"{shop.name},\nне закрыта смена на кассе {cashes}"
        else:
            formated_msg = f"{shop.name},\nне закрыта смена на кассах {cashes}"
        return formated_msg


@dataclass
class TotalMessageEntity:
    sum_by_checks: float
    checks_count: int
    state: str

    def format(self):
        formated_msg = f"Суммарный отчет за {datetime.date.today()}:\nЧеки: {self.checks_count} шт\nОборот: {self.sum_by_checks} руб. "
        if self.state != "{0}":
            return formated_msg
        else:
            return f"{formated_msg}\n(не во всех магазинах закрыты смены)."


@dataclass
class ShopResultEntity:
    sum_by_checks: float
    checks_count: int
    state: str

    def format(self, shop: ShopEntity):
        formated_msg = f"Отчет за {datetime.date.today()} {shop.name}:\nЧеки: {self.checks_count} шт\nОборот: {self.sum_by_checks} руб. "
        if self.state != "{0}":
            return formated_msg
        else:
            return f"{formated_msg}\n(в магазине не все смены закрыты)."
