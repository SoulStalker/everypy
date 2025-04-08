import asyncio

from csi_service.app.constants import KafkaTopics
from csi_service.app.db.engine import session_maker
from csi_service.app.db.orm_query import get_unclosed_shifts
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
        print(f"Недопустимая команда: {command}")
        return

    # Получаем результаты запроса
    unclosed_shifts = await get_unclosed_shifts(session_maker())
    text = {}
    for shift in unclosed_shifts:
        text.setdefault(shift.shopindex, []).append(shift.cashnum)

    response = {"chat_id": chat_id, "message": text}
    send_message(KafkaTopics.CSI_RESPONSES.value, response)
    print(f"Отправлено сообщение: {response}")


async def main():
    print("Запуск слушателя Kafka...")
    for msg in start_consumer(config.kafka.broker, "csi_service"):
        print(f"Получено сообщение: {msg}")
        await process_message(msg)


if __name__ == "__main__":
    asyncio.run(main())
