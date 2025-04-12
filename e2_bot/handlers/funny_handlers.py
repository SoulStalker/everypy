from aiogram import Router, F, Bot
from aiogram.types import Message
from loguru import logger

from e2_bot.configs import load_config
from e2_bot.keyboards import funny_kb

config = load_config('.env')

router = Router()


# Хендлер для сохранения гифок
@router.message(F.animation | F.sticker)
async def handle_animation(message: Message, bot: Bot):
    file_id, content_type = "", ""
    if message.content_type == 'sticker':
        file_id = message.sticker.file_id
        content_type = 'sticker'
    elif message.content_type == 'animation':
        file_id = message.animation.file_id
        content_type = 'animation'
    logger.debug(content_type)
    logger.info(file_id)
    # Сохраняю file_id в базу
    await message.reply(f"GIF сохранён. file_id: {message.content_type}", reply_markup=funny_kb())

    # await bot.send_animation(chat_id=message.chat.id, animation="CgACAgQAAxkBAAILV2f6CeqiIm1nRVQshtrOuszoUWYnAAK2AgACyQsNUyezzCs-co_pNgQ")
    # await bot.send_sticker(chat_id=message.chat.id, sticker="CAACAgIAAxkBAAILSGf6CGhnceMKBC0lIw97BfPQnx4kAAL4JAACrpHASF45skRx5PUtNgQ")
