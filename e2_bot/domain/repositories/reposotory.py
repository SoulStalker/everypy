from e2_bot.domain.entities import USMessageEntity, ShopEntity


class IUnclosedMessageRepository:
    @staticmethod
    def get_formated_message(msg: USMessageEntity) -> str:
        return NotImplemented


class IShopRepository:
    @staticmethod
    def get(number: int) -> ShopEntity:
        raise NotImplementedError
