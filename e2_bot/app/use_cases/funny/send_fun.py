from aiogram import Bot
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from e2_bot.app.data_access.local_db.repository import FunDataRepository
from e2_bot.app.use_cases.funny import GetRandomFunnyUseCase
from e2_bot.configs import load_config

config = load_config('.env')


async def send_funny(bot: Bot, session: AsyncSession):
    logger.success("Sending funny")

    uc = GetRandomFunnyUseCase(FunDataRepository(session))
    result = await uc.execute(answer="bad_boy")
    logger.debug(result)
    await bot.send_sticker(chat_id=config.tg_bot.chat_id, sticker=result.file_id)
