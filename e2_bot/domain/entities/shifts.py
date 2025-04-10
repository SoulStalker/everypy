import base64
import datetime
from dataclasses import dataclass
from pathlib import Path

from loguru import logger

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
