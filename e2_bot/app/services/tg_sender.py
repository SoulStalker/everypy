import asyncio

from aiogram.types import InputFile
from loguru import logger


class TelegramSender:
    def __init__(self, bot, loop):
        self.bot = bot
        self.loop = loop

    def send_message(self, chat_id: int, text: str):
        asyncio.run_coroutine_threadsafe(
            self.bot.send_message(chat_id=chat_id, text=text),
            self.loop
        )

    def send_photo(self, chat_id: int, photo: InputFile, caption: str):
        future = asyncio.run_coroutine_threadsafe(
            self.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                show_caption_above_media=True,
            ),
            self.loop
        )
        try:
            future.result(timeout=15)
        except asyncio.TimeoutError:
            logger.error("Таймаут при отправке фото.")
        except Exception as e:
            logger.error(f"Ошибка: {e}")

    def send_video(self, chat_id: int, video: InputFile, caption: str):
        future = asyncio.run_coroutine_threadsafe(
            self.bot.send_video(
                chat_id=chat_id,
                video=video,
                caption=caption,
                show_caption_above_media=True,
            ),
            self.loop
        )
        try:
            future.result(timeout=15)
        except asyncio.TimeoutError:
            logger.error("Таймаут при отправке фото.")
        except Exception as e:
            logger.error(f"Ошибка: {e}")
