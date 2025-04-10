import asyncio

from aiogram import Bot
from aiogram.types import InputFile, FSInputFile
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter
from loguru import logger

from e2_bot.app.use_cases.handle_message import HandleIncomingAlert, HandleTotalAlert, HandlerResultsAlert, HandleWhatsAppAlert
from e2_bot.configs import load_config
from e2_bot.domain.value_objects.user_command import UserCommand

config = load_config()


def build_kafka_handler(bot: Bot, loop: asyncio.AbstractEventLoop):
    def handler(message: dict):
        chat_id = message.get("chat_id", config.tg_bot.chat_id)
        cmd = message.get("command", "WS")
        content = message.get("content")
        logger.debug(f"Received message: {chat_id} {cmd} ")
        match cmd:
            case UserCommand.UNCLOSED.name:
                shifts_from_kafka = dict(message.get("content", "Пустое сообщение"))
                hia = HandleIncomingAlert()
                if chat_id:
                    for data in shifts_from_kafka.items():
                        payload = {"store_id": data[0], "cashes": data[1]}
                        formatted_shift = hia.execute(payload)
                        asyncio.run_coroutine_threadsafe(
                            bot.send_message(chat_id=chat_id, text=formatted_shift),
                            loop
                        )
            case UserCommand.TOTAL.name:
                hta = HandleTotalAlert()
                asyncio.run_coroutine_threadsafe(
                    bot.send_message(chat_id=chat_id, text=hta.execute(content)),
                    loop
                )
            case UserCommand.RESULTS_BY_SHOP.name:
                hsa = HandlerResultsAlert()
                shifts_from_kafka = dict(message.get("content", "Пустое сообщение"))
                if chat_id:
                    for data in shifts_from_kafka.items():
                        payload = {"store_id": data[0], "results": data[1]}
                        formatted_shift = hsa.execute(payload)
                        asyncio.run_coroutine_threadsafe(
                            bot.send_message(chat_id=chat_id, text=formatted_shift),
                            loop
                        )
            case UserCommand.OTRS_STATS.name:
                chat_id = config.tg_bot.chat_id
                asyncio.run_coroutine_threadsafe(
                    bot.send_message(chat_id=chat_id, text=content),
                    loop
                )
            case UserCommand.EQUIPMENT.name:
                chat_id = config.tg_bot.chat_id
                asyncio.run_coroutine_threadsafe(
                    bot.send_message(chat_id=chat_id, text=content),
                    loop
                )
            case "WS":
                hwa = HandleWhatsAppAlert()
                caption, image_path = hwa.execute(message)
                logger.info(f"caption: {caption}, image_path: {image_path}")
                if caption == "text":
                    asyncio.run_coroutine_threadsafe(
                        bot.send_message(chat_id=chat_id, text=image_path),
                        loop
                    )
                else:
                    photo = FSInputFile(image_path)
                    future = asyncio.run_coroutine_threadsafe(
                        bot.send_photo(
                            chat_id=chat_id,
                            photo=photo,
                            caption=caption,
                            show_caption_above_media=True,
                        ),
                        loop
                    )
                    try:
                        future.result(timeout=15)  # Явно получаем результат
                    except asyncio.TimeoutError:
                        logger.error("Таймаут при отправке фото.")
                    except Exception as e:
                        logger.error(f"Ошибка: {e}")
            case _:
                asyncio.run_coroutine_threadsafe(
                    bot.send_message(chat_id=chat_id, text="unknown message"),
                    loop
                )

    return handler
