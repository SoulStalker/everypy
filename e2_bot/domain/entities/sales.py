import datetime
from dataclasses import dataclass

from e2_bot.domain.entities import ShopEntity


@dataclass
class TotalMessageEntity:
    sum_by_checks: float
    checks_count: int
    state: str

    # def format(self):
    #     formatted_msg = (
    #         f"Суммарный отчет за {datetime.date.today()}:\n"
    #         f"Чеки: {self.checks_count} шт\n"
    #         f"Оборот: {self.sum_by_checks:.2f} руб."
    #     )
    #     if self.state != "{0}":
    #         return formatted_msg
    #     else:
    #         return f"{formatted_msg}\n(не во всех магазинах закрыты смены)."


@dataclass
class TotalMessageFormatter:
    @staticmethod
    def format(checks_count, sum_by_checks, state):
        formatted_msg = (
            f"Суммарный отчет за {datetime.date.today()}:\n"
            f"Чеки: {checks_count} шт\n"
            f"Оборот: {sum_by_checks:.2f} руб."
        )
        if state != "{0}":
            return formatted_msg
        else:
            return f"{formatted_msg}\n(не во всех магазинах закрыты смены)."


@dataclass
class ShopResultEntity:
    sum_by_checks: float
    checks_count: int
    state: str

    # def format(self, shop: ShopEntity):
    #     formatted_msg = (
    #         f"Отчет за {datetime.date.today()}:\n{shop.name}\n"
    #         f"Чеки: {self.checks_count} шт\n"
    #         f"Оборот: {self.sum_by_checks:.2f} руб."
    #     )
    #     if self.state != "{0}":
    #         return formatted_msg
    #     else:
    #         return f"{formatted_msg}\n(в магазине не все смены закрыты)."


@dataclass
class ShopResuFormatter:
    @staticmethod
    def format(shop: ShopEntity, checks_count, sum_by_checks, state):
        formatted_msg = (
            f"Отчет за {datetime.date.today()}:\n{shop.name}\n"
            f"Чеки: {checks_count} шт\n"
            f"Оборот: {sum_by_checks:.2f} руб."
        )
        if state != "{0}":
            return formatted_msg
        else:
            return f"{formatted_msg}\n(в магазине не все смены закрыты)."
