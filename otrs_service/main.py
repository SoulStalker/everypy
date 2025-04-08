import asyncio
import calendar
import datetime

from loguru import logger

from otrs_service.app.db import DataAnalyzer, session_maker
from otrs_service.infrastructure.producer import send_message
from otrs_service.service.service import get_message
from otrs_service.app.constants import KafkaTopics


async def main():
    analyzer = DataAnalyzer(session_maker)
    await analyzer.get_results()
    await analyzer.get_total_open_tickets()

    message, finish = await get_message(analyzer, 'сегодня')
    message += f'\n\nОткрытых заявок осталось: {analyzer.total_open[0][0]}\n\n'
    message += f'Самая старая заявка {analyzer.total_open[0][1]}'
    logger.info(message)
    logger.info(finish)

    # если сегодня воскресенье
    if datetime.datetime.today().weekday() == 6:
        message, finish = get_message(analyzer, 'месяц')

        logger.info(message)
        logger.info(finish)

    # если сегодня последний день месяца
    today = datetime.date.today()
    is_last_day_of_month = today.day == calendar.monthrange(today.year, today.month)[1]
    if is_last_day_of_month:
        message, finish = get_message(analyzer, 'месяц')

        logger.debug(message)
        logger.info(finish)

    send_message(KafkaTopics.OTRS_NOTIFICATIONS.value, {"command": "OTRS_NOTIFICATIONS", "content": message})
    send_message(KafkaTopics.OTRS_NOTIFICATIONS.value, {"command": "OTRS_NOTIFICATIONS", "content": finish})


if __name__ == '__main__':
    asyncio.run(main())
