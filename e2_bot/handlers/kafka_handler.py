from aiogram import Bot


def build_kafka_handler(bot: Bot):
    def handler(message: dict):
        chat_id = message.get("chat_id")
        text = message.get("text", "Получено сообщение")

        if chat_id:
            asyncio.run_coroutine_threadsafe(
                bot.send_message(chat_id=chat_id, text=text),
                asyncio.get_event_loop()
            )

    return handler
