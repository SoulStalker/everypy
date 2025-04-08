import asyncio

from aiogram import Bot, Dispatcher

from e2_bot.app.constants import KafkaTopics
from e2_bot.configs import load_config
from e2_bot.handlers import router
from e2_bot.handlers.kafka_handler import build_kafka_handler
from e2_bot.infrastructure.consumer import KafkaMessageReceiver
from e2_bot.keyboards import set_main_menu
from e2_bot.middlewares import ShadowBanMiddleware


async def main():
    config = load_config('.env')
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    await set_main_menu(bot)

    dp.include_router(router)

    dp.update.middleware(ShadowBanMiddleware(config.tg_bot.admin_ids))

    # Инициализируем Kafka receiver
    csi_receiver = KafkaMessageReceiver(
        topic=KafkaTopics.CSI_RESPONSES.value,
        bootstrap_servers=config.kafka.broker,
        group_id="csi_service"
    )

    otrs_receiver = KafkaMessageReceiver(
        topic=KafkaTopics.OTRS_STATS.value,
        bootstrap_servers=config.kafka.broker,
        group_id="otrs_service"
    )

    # Передаём боту хендлер, который будет обрабатывать сообщения из Kafka
    # main.py
    loop = asyncio.get_running_loop()
    csi_handler = build_kafka_handler(bot, loop)
    otrs_handler = build_kafka_handler(bot, loop)

    # Запускаем консюмера в фоне
    asyncio.create_task(csi_receiver.consume(csi_handler))
    asyncio.create_task(otrs_receiver.consume(otrs_handler))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
