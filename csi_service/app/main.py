import asyncio

from loguru import logger

from csi_service.app.constants import KafkaTopics
from csi_service.app.db.engine import session_maker
from csi_service.app.db.orm_query import get_unclosed_shifts, get_results_by_shop
from csi_service.app.user_commands import UserCommands
from csi_service.configs import load_config
from csi_service.infrastructure.consumer import start_consumer
from csi_service.infrastructure.producer import send_message

config = load_config('.env')


async def process_message(msg: dict):
    chat_id = msg.get("chat_id")
    command = msg.get("command")

    # Проверяем, что команда допустимая
    if command not in [cmd.name for cmd in UserCommands]:
        logger.error(f"Недопустимая команда: {command}")
        return

    response = {"chat_id": chat_id, "command": command, "content": "unknown command"}
    # Получаем результаты запроса
    if command == UserCommands.UNCLOSED.name:
        unclosed_shifts = await get_unclosed_shifts(session_maker())
        content = {}
        for shift in unclosed_shifts:
            content.setdefault(shift.shopindex, []).append(shift.cashnum)
        response["content"] = content
    elif command == UserCommands.TOTAL.name:
        total = await get_results_by_shop(session_maker())
        summary = total.get('total_summary', 0)
        summary["state"] = str(summary["state"])
        response["content"] = summary
    elif command == UserCommands.RESULTS_BY_SHOP.name:
        results = await get_results_by_shop(session_maker())
        logger.debug(results)
        response["content"] = results
    send_message(KafkaTopics.TG_BOT_MSGS.value, response)
    logger.debug(f"Отправлено сообщение в топик: {KafkaTopics.TG_BOT_MSGS.value}")


async def main():
    logger.info("Запуск слушателя Kafka...")
    for msg in start_consumer(config.kafka.broker, "csi_service"):
        logger.debug(f"Получено сообщение: {msg}")
        await process_message(msg)


if __name__ == "__main__":
    asyncio.run(main())
