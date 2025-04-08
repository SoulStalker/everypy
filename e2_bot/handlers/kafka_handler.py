import asyncio

from aiogram import Bot


def build_kafka_handler(bot: Bot, loop: asyncio.AbstractEventLoop):
    def handler(message: dict):
        chat_id = message.get("chat_id")
        text = message.get("text", "Получено сообщение")

        if chat_id:
            asyncio.run_coroutine_threadsafe(
                bot.send_message(chat_id=chat_id, text=text),
                loop
            )

    return handler
