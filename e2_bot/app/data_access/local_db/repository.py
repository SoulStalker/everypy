from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from e2_bot.domain.entities import WhatsAppContact, WhatsAppGroup
from e2_bot.domain.repositories import IWAContactRepository, IWAGroupRepository
from .mappers import gr_model_to_dto, ct_model_to_dto, ct_dto_to_model, gr_dto_to_model
from .models import Group, Contact


class WAContactRepository(IWAContactRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.wa_contact = Contact

    async def get(self, number: int) -> WhatsAppContact | None:
        result = await self.session.get(self.wa_contact, number)
        if result:
            return ct_model_to_dto(result)
        return None

    async def get_all(self):
        # Реализация аналогично get, но с выборкой всех записей
        pass

    async def add(self, contact: WhatsAppContact):
        model = ct_dto_to_model(contact)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)


class WAGroupRepository(IWAGroupRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.wa_group = Group

    async def get(self, number: int) -> WhatsAppGroup:
        model = await self.session.get(self.wa_group, number)
        return gr_model_to_dto(model)

    async def get_all(self):
        result = await self.session.execute(select(self.wa_group))
        models = result.scalars().all()
        return [gr_model_to_dto(model).__str__() for model in models]

    async def add(self, gr: WhatsAppGroup):
        wa_group = gr_dto_to_model(gr)
        self.session.add(wa_group)
        await self.session.commit()
        await self.session.refresh(wa_group)
