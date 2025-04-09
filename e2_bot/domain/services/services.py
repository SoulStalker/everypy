from e2_bot.domain.entities.shift_message import USMessageEntity
from e2_bot.domain.entities.shopentity import ShopEntity
from e2_bot.domain.repositories import IUnclosedMessageRepository, IShopRepository


class UnclosedMessageService:
    def __init__(self, repository: IUnclosedMessageRepository):
        self.repository = repository

    def get_formated_message(self, msg: USMessageEntity, shop: ShopEntity):
        cashes = ",".join(map(str, msg.cashes))
        if len(msg.cashes) == 1:
            formatted_msg = f"{shop.name},\nне закрыта смена на кассе {cashes}"
        else:
            formatted_msg = f"{shop.name},\nне закрыта смена на кассах {cashes}"
        return formatted_msg


class ShopService:
    def __init__(self, repository: IShopRepository):
        self.repository = repository

    def get(self, number: int):
        return self.repository.get(number)