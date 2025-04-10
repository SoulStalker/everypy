from e2_bot.domain.entities import USMessageEntity, WhatsAppGroup, WhatsAppContact
from e2_bot.domain.repositories import IUnclosedMessageRepository, IShopRepository, IWAContactRepository, IWAGroupRepository


class UnclosedMessageService:
    def __init__(self, repository: IUnclosedMessageRepository):
        self.repository = repository

    def get_formated_message(self, msg: USMessageEntity) -> str:
        return self.repository.get_formated_message(msg)


class ShopService:
    def __init__(self, repository: IShopRepository):
        self.repository = repository

    def get(self, number: int):
        return self.repository.get(number)


class WAGroupService:
    def __init__(self, repository: IWAGroupRepository):
        self.repository = repository

    def get(self, number: int):
        return self.repository.get(number)

    def get_all(self):
        return self.repository.get_all()

    def add(self, group: WhatsAppGroup):
        return self.repository.add(group)

    def update(self, group: WhatsAppGroup):
        return self.repository.update(group)

    def delete(self, group: WhatsAppGroup):
        return self.repository.delete(group)


class WAContactService:
    def __init__(self, repository: IWAContactRepository):
        self.repository = repository

    def get(self, number: int):
        return self.repository.get(number)

    def get_all(self):
        return self.repository.get_all()

    def add(self, contact: WhatsAppContact):
        return self.repository.add(contact)

    def update(self, contact: WhatsAppContact):
        return self.repository.update(contact)

    def delete(self, contact: WhatsAppContact):
        return self.repository.delete(contact)
