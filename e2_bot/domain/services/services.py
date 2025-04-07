from e2_bot.domain.entities.shift_message import UnclosedShiftMessageEntity
from e2_bot.domain.entities.shop import Shop
from e2_bot.domain.repositories import IUnclosedMessageRepository, IShopRepository


class UnclosedMessageService:
    def __init__(self, repository: IUnclosedMessageRepository):
        self.repository = repository

    def get_formated_message(self, msg: UnclosedShiftMessageEntity, shop: Shop):
        cashes = ",".join(map(str, msg.cashes))
        if len(msg.cashes) == 1:
            formated_msg = f"{shop.name},\nне закрыта смена на кассе {cashes}"
        else:
            formated_msg = f"{shop.name},\nне закрыта смена на кассах {cashes}"
        return formated_msg


class ShopService:
    def __init__(self, repository: IShopRepository):
        self.repository = repository

    def get(self, number: int):
        return self.repository.get(number)