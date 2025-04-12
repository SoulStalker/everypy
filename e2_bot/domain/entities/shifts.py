from dataclasses import dataclass


from e2_bot.domain.entities import ShopEntity


@dataclass
class USMessageEntity:
    """
    Сущность для хранения данных о не закрытых сменах
    """
    shop_number: int
    cashes: [int]

    def format(self, shop: ShopEntity):
        cashes = ", ".join(map(str, self.cashes))
        status = False
        if shop:
            if len(self.cashes) == 0:
                formatted_msg, status = "<i>Все смены закрыты</i>", True
            elif len(self.cashes) == 1:
                formatted_msg = f"<i>{shop.name},\nне закрыта смена на кассе {cashes}</i>"
            else:
                formatted_msg = f"<i>{shop.name},\nне закрыта смена на кассах {cashes}</i>"
        else:
            formatted_msg = "<b>Проблема с получением адреса магазина</b>"
        return formatted_msg, status
