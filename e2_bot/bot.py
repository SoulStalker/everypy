import asyncio

from aiogram import Bot, Dispatcher

from e2_bot.configs.config import load_config


async def main():
    config = load_config('.env')
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
