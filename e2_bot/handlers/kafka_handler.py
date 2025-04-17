import asyncio

from aiogram import Bot
from aiogram.types import FSInputFile
from loguru import logger

from e2_bot.app.constants import TgAnswer
from e2_bot.app.services.tg_sender import TelegramSender
from e2_bot.app.use_cases.funny.send_fun import send_funny
from e2_bot.app.use_cases.message_handler_factory import MessageHandlerFactory
from e2_bot.configs import load_config
from e2_bot.domain.value_objects.content_types import ContentTypes
from e2_bot.domain.value_objects.user_command import UserCommand
from e2_bot.lexicon import LEXICON

config = load_config()


def build_kafka_handler(bot: Bot, loop: asyncio.AbstractEventLoop):
    tg_sender = TelegramSender(bot, loop)

    def handle_message(message: dict):
        chat_id = message.get("chat_id", config.tg_bot.chat_id)
        cmd = message.get("command", "WS")
        content = message.get("content")
        logger.debug(f"Received message: {chat_id} {cmd}")
        logger.info(f"Message struct: {message.keys()}")
        logger.info(f"Message: {message}")
        handler = MessageHandlerFactory.get_handler(cmd)
        match cmd:
            case UserCommand.UNCLOSED.name:
                if not content:
                    tg_sender.send_message(chat_id=chat_id, text=LEXICON['all_closed'])
                if chat_id:
                    for data in content.items():
                        payload = {"store_id": data[0], "cashes": data[1]}
                        formatted_shift = asyncio.run(handler.execute(payload))
                        tg_sender.send_message(chat_id=chat_id, text=formatted_shift)

            case UserCommand.TOTAL.name:
                tg_sender.send_message(chat_id=chat_id, text=asyncio.run(handler.execute(content)))

            case UserCommand.RESULTS_BY_SHOP.name:
                for data in content.items():
                    logger.debug(f"Received message: {chat_id} {data}")
                    payload = {"store_id": data[0], "results": data[1]}
                    tg_sender.send_message(chat_id=chat_id, text=handler.execute(payload))

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
                    tg_sender.send_message(chat_id=chat_id, text=content)

            case UserCommand.OTRS_NEW_TICKET.name:
                chat_id = config.tg_bot.chat_id
                tg_sender.send_message(chat_id=chat_id, text=content)

            case UserCommand.EQUIPMENT.name:
                chat_id = config.tg_bot.chat_id
                tg_sender.send_message(chat_id=chat_id, text=content)

            case UserCommand.WS.name:
                # hwa = WSMessageHandler()
                caption, data = handler.execute(message)
                logger.info(f"caption: {caption}, file_path: {data}")
                ct = message.get("content_type")
                match ct:
                    case ContentTypes.TEXT.value | ContentTypes.ETEXT.value:
                        tg_sender.send_message(chat_id=chat_id, text=data)

                    case ContentTypes.IMAGE.value:
                        photo = FSInputFile(data)
                        tg_sender.send_photo(chat_id=chat_id, photo=photo, caption=caption)
                    case ContentTypes.VIDEO.value:
                        video = FSInputFile(data)
                        tg_sender.send_video(chat_id=chat_id, video=video, caption=caption)
                    case _:
                        logger.error(f"Unknown message type: {ct}")
            case _:
                tg_sender.send_message(chat_id=chat_id, text="Unknown command")

    return handle_message
