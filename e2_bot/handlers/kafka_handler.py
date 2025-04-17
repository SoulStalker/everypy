import asyncio

from aiogram import Bot
from aiogram.types import FSInputFile
from loguru import logger

from e2_bot.app.constants import TgAnswer
from e2_bot.app.use_cases.funny.send_fun import send_funny
from e2_bot.app.use_cases.handle_message import HandleIncomingAlert, HandleTotalAlert, HandlerResultsAlert, HandleWhatsAppAlert
from e2_bot.configs import load_config
from e2_bot.domain.value_objects.content_types import ContentTypes
from e2_bot.domain.value_objects.user_command import UserCommand
from e2_bot.lexicon import LEXICON

config = load_config()


def build_kafka_handler(bot: Bot, loop: asyncio.AbstractEventLoop):
    def handler(message: dict):
        chat_id = message.get("chat_id", config.tg_bot.chat_id)
        cmd = message.get("command", "WS")
        content = message.get("content")
        logger.debug(f"Received message: {chat_id} {cmd}")
        logger.info(f"Message struct: {message.keys()}")
        logger.info(f"Message: {message}")
        match cmd:
            case UserCommand.UNCLOSED.name:
                shifts_from_kafka = dict(message.get("content", "Пустое сообщение"))
                if not shifts_from_kafka:
                    asyncio.run_coroutine_threadsafe(
                        bot.send_message(chat_id=chat_id, text=LEXICON['all_closed']),
                        loop
                    )
                    asyncio.run_coroutine_threadsafe(
                        send_funny(bot, answer=TgAnswer.ALL_CLOSED.value),
                        loop)
                hia = HandleIncomingAlert()
                if chat_id:
                    for data in shifts_from_kafka.items():
                        payload = {"store_id": data[0], "cashes": data[1]}
                        formatted_shift = asyncio.run(hia.execute(payload))
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
                if content == TgAnswer.GOOD_BOY.value:
                    asyncio.run_coroutine_threadsafe(
                        send_funny(bot, answer=TgAnswer.GOOD_BOY.value),
                        loop
                    )
                elif content == TgAnswer.BAD_BOY.value:
                    asyncio.run_coroutine_threadsafe(
                        send_funny(bot, answer=TgAnswer.BAD_BOY.value),
                        loop
                    )
                else:
                    asyncio.run_coroutine_threadsafe(
                        bot.send_message(chat_id=chat_id, text=content),
                        loop
                    )
            case UserCommand.OTRS_NEW_TICKET.name:
                logger.error(f"Processing message {content}")
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
                ct = message.get("content_type")
                match ct:
                    case ContentTypes.TEXT.value | ContentTypes.ETEXT.value:
                        logger.info(f"Message text: {ct}")
                    case ContentTypes.IMAGE.value:
                        logger.info(f"Message image: {image_path}")
                    case ContentTypes.VIDEO.value:
                        logger.info(f"Message video: {image_path}")
                    case _:
                        logger.error(f"Unknown message type: {ct}")
                if caption == "text":
                    asyncio.run_coroutine_threadsafe(
                        bot.send_message(chat_id=chat_id, text=image_path),
                        loop
                    )
                elif message.get("content_type", "") == "video/mp4":
                    video = FSInputFile(image_path)
                    future = asyncio.run_coroutine_threadsafe(
                        bot.send_video(
                            chat_id=chat_id,
                            video=video,
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
                else:
                    logger.warning(f"message content type is {message.get('content_type', '')}")
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
                    bot.send_message(chat_id=chat_id, text=LEXICON.get("unknown message")),
                    loop
                )

    return handler
