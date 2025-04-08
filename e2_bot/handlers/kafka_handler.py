import asyncio

from aiogram import Bot
from loguru import logger

from e2_bot.app.use_cases.handle_message import HandleIncomingAlert, HandleTotalAlert


def build_kafka_handler(bot: Bot, loop: asyncio.AbstractEventLoop):
    def handler(message: dict):
        chat_id = message.get("chat_id")
        cmd = message.get("command")
        content = message.get("content")
        logger.debug(f"Received message: {chat_id} {cmd} {content}")
        match cmd:
            case "UNCLOSED":
                shifts_from_kafka = dict(message.get("content", "Получено сообщение"))
                hia = HandleIncomingAlert()
                if chat_id:
                    for data in shifts_from_kafka.items():
                        payload = {"store_id": data[0], "cashes": data[1]}
                        formatted_shift = hia.execute(payload)
                        asyncio.run_coroutine_threadsafe(
                            bot.send_message(chat_id=chat_id, text=formatted_shift),
                            loop
                        )
            case "TOTAL":
                hta = HandleTotalAlert()
                asyncio.run_coroutine_threadsafe(
                    bot.send_message(chat_id=chat_id, text=hta.execute(content)),
                    loop
                )
            case _:
                asyncio.run_coroutine_threadsafe(
                    bot.send_message(chat_id=chat_id, text="unknown command"),
                    loop
                )
    return handler
