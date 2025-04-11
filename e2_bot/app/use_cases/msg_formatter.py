from e2_bot.app.data_access import WAContactRepository
from e2_bot.app.data_access.local_db import session_maker
from e2_bot.app.use_cases import GetModelUseCase
from e2_bot.domain.entities import WhatsAppMessageEntity


class MessageFormatter:
    @classmethod
    async def execute(cls, entity: WhatsAppMessageEntity):
        time_stamp = entity.time_stamp.strftime("%d.%m.%Y, %H:%M:%S")
        formatted_msg = f"Сообщение в группе {entity.group}\n[{time_stamp}] {entity.sender}: {entity.content}"
        async with session_maker() as session:
            repo = WAContactRepository(session)
            uc = GetModelUseCase(repo)
            contact = await uc.execute(entity.sender)
            sender_name = f"{contact.first_name} {contact.last_name}"
            if contact:
                formatted_msg = f"Сообщение в группе {entity.group}\n[{time_stamp}] {sender_name}: {entity.content}"
        return formatted_msg
