from aiogram import Router, F, Bot
from aiogram.types import Message
from loguru import logger

from e2_bot.configs import load_config

config = load_config('.env')

router = Router()


# Хендлер для сохранения гифок
@router.message(F.animation)
async def handle_animation(message: Message, bot: Bot):
    gif_id = message.animation.file_id
    logger.info(gif_id)
    # Сохраняю file_id в базу
    await message.reply(f"GIF сохранён. file_id: {gif_id}")
    await bot.send_animation(chat_id=message.chat.id, animation="CgACAgQAAxkBAAILV2f6CeqiIm1nRVQshtrOuszoUWYnAAK2AgACyQsNUyezzCs-co_pNgQ")


# Хендлер для сохранения стикеров
@router.message(F.sticker)
async def handle_sticker(message: Message, bot: Bot):
    sticker_id = message.sticker.file_id
    logger.info(sticker_id)
    # Сохраняю file_id в базу
    await message.reply(f"Стикер сохранён. file_id: {sticker_id}")
    await bot.send_sticker(chat_id=message.chat.id, sticker="CAACAgIAAxkBAAILSGf6CGhnceMKBC0lIw97BfPQnx4kAAL4JAACrpHASF45skRx5PUtNgQ")
