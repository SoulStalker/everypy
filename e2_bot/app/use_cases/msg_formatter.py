from e2_bot.app.data_access import WAContactRepository, WAGroupRepository
from e2_bot.app.data_access.local_db import session_maker
from e2_bot.domain.entities import WhatsAppMessageEntity
from e2_bot.domain.value_objects.content_types import ContentTypes
from .wa_groups import GetModelUseCase


class MessageFormatter:
    @classmethod
    async def execute(cls, entity: WhatsAppMessageEntity):
        sender_name = entity.sender
        time_stamp = entity.time_stamp.strftime("%d.%m.%Y, %H:%M:%S")
        formatted_msg = f"🔔 <b>{entity.group}</b>\n<i>{time_stamp}</i>\n<b>{entity.sender}:</b>"
        async with session_maker() as session:
            c_repo = WAContactRepository(session)
            g_repo = WAGroupRepository(session)
            ucc = GetModelUseCase(c_repo)
            contact = await ucc.execute(entity.sender)
            ucg = GetModelUseCase(g_repo)
            group = await ucg.execute(entity.group)
            if contact:
                sender_name = f"{contact.first_name} {contact.last_name}"
                formatted_msg = f"🔔 <b>{entity.group}</b>\n<i>{time_stamp}</i>\n<b>{sender_name}:</b>"
            if group:
                from_group = group.group_name
                formatted_msg = f"🔔 <b>{from_group}</b>\n<i>{time_stamp}</i>\n<b>{sender_name}:\n</b>"
        if entity.content_type == ContentTypes.TEXT.value or entity.content_type == ContentTypes.ETEXT.value:
            formatted_msg += f"{entity.content}"
        return formatted_msg
