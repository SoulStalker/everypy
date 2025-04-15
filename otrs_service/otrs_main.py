import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from otrs_service.configs import load_config
from otrs_service.infrastructure.consumer import consume
from otrs_service.service.service import check_new_tickets

config = load_config('.env')


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_new_tickets, 'interval', minutes=5)
    scheduler.start()

    logger.info("Запуск слушателя Kafka...")
    await consume(config.kafka.broker, "csi_service")


if __name__ == "__main__":
    asyncio.run(main())
