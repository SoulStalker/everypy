from e2_bot.domain.entities.shift_message import UnclosedShiftMessageEntity
from e2_bot.domain.repositories import IUnclosedMessageRepository, IShopRepository


class UnclosedMessageService:
    def __init__(self, repository: IUnclosedMessageRepository):
        self.repository = repository

    def get_formated_message(self, msg: UnclosedShiftMessageEntity):
        return self.repository.get_formated_message(msg)


class ShopService:
    def __init__(self, repository: IShopRepository):
        self.repository = repository

    def get(self, number: int):
        return self.repository.get(number)