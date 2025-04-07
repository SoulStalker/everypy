import asyncio

from aiogram import Bot, Dispatcher

from e2_bot.configs import load_config
from e2_bot.handlers import router
from e2_bot.keyboards import set_main_menu


async def main():
    config = load_config('.env')
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    await set_main_menu(bot)

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
