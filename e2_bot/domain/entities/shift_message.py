from dataclasses import dataclass

from e2_bot.domain.entities import ShopEntity


@dataclass
class USMessageEntity:
    shop_number: int
    cashes: [int]

    def format(self, shop: ShopEntity):
        cashes = ",".join(map(str, self.cashes))
        if len(self.cashes) == 1:
            formated_msg = f"{shop.name},\nне закрыта смена на кассе {cashes}"
        else:
            formated_msg = f"{shop.name},\nне закрыта смена на кассах {cashes}"
        return formated_msg
