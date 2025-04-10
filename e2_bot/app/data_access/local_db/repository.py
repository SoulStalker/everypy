from sqlalchemy.ext.asyncio import AsyncSession

from e2_bot.domain.entities import WhatsAppContact
from e2_bot.domain.repositories import IWAContactRepository, IWAGroupRepository

from .models import Group, Contact


class WAContactRepository(IWAContactRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.wa_contact = Contact  # Предполагается, что это модель SQLAlchemy

    async def get(self, number: int) -> WhatsAppContact | None:
        result = await self.session.get(self.wa_contact, number)
        if result:
            return WhatsAppContact(
                phone_number=result.phone_number,
                first_name=result.first_name,
                last_name=result.last_name,
                email=result.email,
                telegram_id=result.telegram_id
            )
        return None

    async def get_all(self):
        # Реализация аналогично get, но с выборкой всех записей
        pass

    async def add(self, contact: WhatsAppContact):
        model = self.wa_contact(
            phone_number=contact.phone_number,
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            telegram_id=contact.telegram_id
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)  # если нужно обновить модель


class WAGroupRepository(IWAGroupRepository):
    wa_group = Group

    def __init__(self, session: AsyncSession):
        self.session = session

