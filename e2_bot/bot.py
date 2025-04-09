import asyncio

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from e2_bot.app.constants import KafkaTopics
from e2_bot.app.services.notifcation_sender import send_otrs_notifications, send_unclosed_notifications
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
    kafka_receiver = KafkaMessageReceiver(
        topic=KafkaTopics.TG_BOT_MSGS.value,
        bootstrap_servers=config.kafka.broker,
        group_id="csi_service"
    )

    # Передаём боту хендлер, который будет обрабатывать сообщения из Kafka
    loop = asyncio.get_running_loop()
    kafka_handler = build_kafka_handler(bot, loop)

    # Запускаем консюмера в фоне
    asyncio.create_task(kafka_receiver.consume(kafka_handler))

    # 🕒 Настраиваем планировщик задач
    scheduler = AsyncIOScheduler()

    # Пример: 3 уведомления в день в определённое время
    scheduler.add_job(
        send_otrs_notifications,
        CronTrigger(hour=13, minute=00),
    )
    scheduler.add_job(
        send_otrs_notifications,
        CronTrigger(hour=18, minute=0),
    )
    scheduler.add_job(
        send_unclosed_notifications,
        CronTrigger(hour=23, minute=15),
    )
    scheduler.add_job(
        send_unclosed_notifications,
        CronTrigger(hour=23, minute=25),
    )
    scheduler.add_job(
        send_otrs_notifications,
        CronTrigger(hour=23, minute=30),
    )
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
