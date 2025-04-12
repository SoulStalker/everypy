from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from e2_bot.domain.entities import WhatsAppContact, WhatsAppGroup, FunData
from e2_bot.domain.repositories import IWAContactRepository, IWAGroupRepository, IFunDataRepository
from e2_bot.lexicon import LEXICON
from .mappers import gr_model_to_dto, ct_model_to_dto, ct_dto_to_model, gr_dto_to_model, funny_model_to_dto
from .models import Group, Contact, Funny

from loguru import logger


class WAContactRepository(IWAContactRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.wa_contact = Contact

    async def get(self, phone: int) -> WhatsAppContact | None:
        model = await self.session.get(self.wa_contact, phone)
        if model:
            return ct_model_to_dto(model)
        return None

    async def get_all(self):
        result = await self.session.execute(select(self.wa_contact))
        models = result.scalars().all()
        return [ct_model_to_dto(model).__str__() for model in models]

    async def add(self, ct: WhatsAppContact):
        if await self.get(ct.phone_number):
            return ct, LEXICON.get('contact_exists')
        wa_contact = ct_dto_to_model(ct)
        self.session.add(wa_contact)
        await self.session.commit()
        await self.session.refresh(wa_contact)
        return ct_model_to_dto(wa_contact), None


class WAGroupRepository(IWAGroupRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.wa_group = Group

    async def get(self, number: int) -> WhatsAppGroup | None:
        model = await self.session.get(self.wa_group, number)
        if model:
            return gr_model_to_dto(model)
        return None

    async def get_all(self):
        result = await self.session.execute(select(self.wa_group))
        models = result.scalars().all()
        return [gr_model_to_dto(model).__str__() for model in models]

    async def add(self, gr: WhatsAppGroup):
        if await self.get(gr.group_id):
            return gr, LEXICON['group_exists']
        wa_group = gr_dto_to_model(gr)
        self.session.add(wa_group)
        await self.session.commit()
        await self.session.refresh(wa_group)
        return gr_model_to_dto(wa_group), None


class FunDataRepository(IFunDataRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.funny = Funny

    async def get_random(self, answer: str, content_type: str = None):
        stmt = select(self.funny).where(self.funny.answer == answer)

        if content_type is not None:
            stmt = stmt.where(self.funny.content_type == content_type)

        stmt = stmt.order_by(func.random()).limit(1)

        result = await self.session.execute(stmt)
        model = result.scalars().first()

        logger.info(f"Random model: {model}")

        if model:
            return funny_model_to_dto(model)
        return None

    async def add(self, data: FunData):
        funny = Funny(
            content_type=data.content_type,
            file_id=data.file_id,
            answer=data.answer,
        )
        self.session.add(funny)
        await self.session.commit()
        await self.session.refresh(funny)
        return funny_model_to_dto(funny)
