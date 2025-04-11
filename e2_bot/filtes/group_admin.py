from loguru import logger
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ChatType


class IsGroupAdmin(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        # Получаем объект сообщения
        message = event.message if isinstance(event, CallbackQuery) else event
        logger.debug(f"Получено сообщение: {message}")
        # Проверяем, что сообщение из группы или супергруппы
        if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE]:
            logger.warning("Сообщение не из группы или супергруппы")
            return False
        try:
            logger.info("Получаем список администраторов чата")
            admins = await message.bot.get_chat_administrators(message.chat.id)
            admin_ids = [admin.user.id for admin in admins]
            logger.error(message.from_user.id in admin_ids)
            logger.info(message.from_user.id)

            return any(admin.user.id == message.from_user.id for admin in admins)
        except Exception as e:
            logger.error(f"Ошибка при получении администраторов чата: {e}")
            return False
