from e2_bot.domain.entities import UnclosedShiftMessageEntity, Shop


class IUnclosedMessageRepository:
    @staticmethod
    def get_formated_message(msg: UnclosedShiftMessageEntity) -> str:
        return NotImplemented


class IShopRepository:
    @staticmethod
    def get(number: int) -> Shop:
        raise NotImplementedError
