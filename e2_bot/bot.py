import asyncio

from aiogram import Bot, Dispatcher

from e2_bot.configs import load_config
from e2_bot.handlers import router
from e2_bot.keyboards import set_main_menu
from e2_bot.middlewares import ShadowBanMiddleware


async def main():
    config = load_config('.env')
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    await set_main_menu(bot)

    dp.include_router(router)

    dp.update.middleware(ShadowBanMiddleware(config.tg_bot.admin_ids))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
