import datetime
from dataclasses import dataclass

from e2_bot.domain.entities import ShopEntity


@dataclass
class USMessageEntity:
    shop_number: int
    cashes: [int]

    def format(self, shop: ShopEntity):
        cashes = ", ".join(map(str, self.cashes))
        if shop:
            if len(self.cashes) == 0:
                formatted_msg = f"Все смены закрыты"
            elif len(self.cashes) == 1:
                formatted_msg = f"{shop.name},\nне закрыта смена на кассе {cashes}"
            else:
                formatted_msg = f"{shop.name},\nне закрыта смена на кассах {cashes}"
        else:
            formatted_msg = f"Проблема с получением адреса магазина"
        return formatted_msg


@dataclass
class TotalMessageEntity:
    sum_by_checks: float
    checks_count: int
    state: str

    def format(self):
        formatted_msg = (
            f"Суммарный отчет за {datetime.date.today()}:\n"
            f"Чеки: {self.checks_count} шт\n"
            f"Оборот: {self.sum_by_checks:.2f} руб."
        )
        if self.state != "{0}":
            return formatted_msg
        else:
            return f"{formatted_msg}\n(не во всех магазинах закрыты смены)."


@dataclass
class ShopResultEntity:
    sum_by_checks: float
    checks_count: int
    state: str

    def format(self, shop: ShopEntity):
        formatted_msg = (
            f"Суммарный отчет за {datetime.date.today()}:\n"
            f"Чеки: {self.checks_count} шт\n"
            f"Оборот: {self.sum_by_checks:.2f} руб."
        )
        if self.state != "{0}":
            return formatted_msg
        else:
            return f"{formatted_msg}\n(в магазине не все смены закрыты)."
