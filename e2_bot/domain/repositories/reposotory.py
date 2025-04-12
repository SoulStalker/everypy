from e2_bot.domain.entities import USMessageEntity, ShopEntity, WhatsAppGroup, WhatsAppContact, FunData


class IUnclosedMessageRepository:
    @staticmethod
    def format(msg: USMessageEntity) -> str:
        return NotImplemented


class IShopRepository:
    @staticmethod
    def get(number: int) -> ShopEntity:
        raise NotImplementedError


class IWAContactRepository:
    @staticmethod
    def get(number: int) -> WhatsAppContact:
        raise NotImplementedError

    @staticmethod
    def get_all() -> [WhatsAppContact]:
        raise NotImplementedError

    @staticmethod
    def add(contact: WhatsAppContact):
        raise NotImplementedError

    @staticmethod
    def update(contact: WhatsAppContact):
        raise NotImplementedError

    @staticmethod
    def delete(contact: WhatsAppContact):
        raise NotImplementedError


class IWAGroupRepository:
    @staticmethod
    def get(number: int) -> WhatsAppGroup:
        raise NotImplementedError

    @staticmethod
    def get_all() -> [WhatsAppGroup]:
        raise NotImplementedError

    @staticmethod
    def add(group: WhatsAppGroup):
        raise NotImplementedError

    @staticmethod
    def update(group: WhatsAppGroup):
        raise NotImplementedError

    @staticmethod
    def delete(group: WhatsAppGroup):
        raise NotImplementedError


class IFunDataRepository:
    @staticmethod
    def get() -> FunData:
        raise NotImplementedError

    @staticmethod
    def add(data: FunData):
        raise NotImplementedError
