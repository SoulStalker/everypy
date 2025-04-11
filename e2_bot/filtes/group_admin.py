from loguru import logger
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ChatType

from e2_bot.configs import load_config

config = load_config('.env')


class IsGroupAdmin(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        message = event.message if isinstance(event, CallbackQuery) else event
        logger.debug(f"Получено сообщение: {message}")

        if message.chat.type == ChatType.PRIVATE:
            logger.info("Сообщение из личного чата")
            logger.debug(event.from_user.id)
            logger.error(config.tg_bot.owner_id)
            if event.from_user.id == config.tg_bot.owner_id:
                return True
            return False
        elif message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            logger.warning("Сообщение не из группы или супергруппы")
            return False
        try:
            logger.info("Получаем список администраторов чата")
            admins = await message.bot.get_chat_administrators(message.chat.id)
            admin_ids = [admin.user.id for admin in admins]
            logger.error(event.from_user.id in admin_ids)
            logger.info(event.from_user.id)

            return any(admin.user.id == message.from_user.id for admin in admins)
        except Exception as e:
            logger.error(f"Ошибка при получении администраторов чата: {e}")
            return False
