import asyncio


class TelegramSender:
    def __init__(self, bot, loop):
        self.bot = bot
        self.loop = loop

    def send_message(self, chat_id: int, text: str):
        asyncio.run_coroutine_threadsafe(
            self.bot.send_message(chat_id=chat_id, text=text),
            self.loop
        )
