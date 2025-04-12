from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from e2_bot.app.data_access.local_db import session_maker
from e2_bot.app.data_access.local_db.repository import FunDataRepository
from e2_bot.app.use_cases.funny import GetRandomFunnyUseCase
from e2_bot.configs import load_config

config = load_config('.env')


async def send_funny(bot: Bot, session: AsyncSession = session_maker(), answer: str = "all_closed"):
    uc = GetRandomFunnyUseCase(FunDataRepository(session))
    result = await uc.execute(answer=answer)
    if result is None:
        return
    await bot.send_sticker(chat_id=config.tg_bot.chat_id, sticker=result.file_id)
