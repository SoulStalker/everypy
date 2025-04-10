from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from loguru import logger

from e2_bot.app.constants import KafkaTopics
from e2_bot.configs import load_config
from e2_bot.domain.value_objects import UserCommand
from e2_bot.infrastructure.producer import KafkaMessageSender
from e2_bot.lexicon import LEXICON

config = load_config('.env')

router = Router()
producer = KafkaMessageSender(config.kafka.broker)


# Этот хендлер срабатывает на команду /start и создает пользователя в базе данных
@router.message(CommandStart())
async def start_command(message: Message, bot: Bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text=LEXICON['/start'],
    )


# Этот хендлер срабатывает на команду /help
@router.message(Command('help'))
async def help_command(message: Message, bot: Bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text=LEXICON['/help'],
    )


# Этот хендлер срабатывает на команду /service
@router.message(Command('service'))
async def support_command(message: Message, bot: Bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{LEXICON['/service']}"
    )


# Этот хендлер срабатывает на команду /contacts
@router.message(Command('contacts'))
async def contacts_command(message: Message, bot: Bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text=LEXICON['/contacts'],
    )


# Этот хендлер срабатывает на команду /unclosed
@router.message(Command('unclosed'))
async def unclosed_command(message: Message, bot: Bot):
    payload = {"chat_id": message.chat.id, "command": UserCommand.UNCLOSED.name}
    producer.send(KafkaTopics.USER_COMMANDS.value, payload)


# Этот хендлер срабатывает на команду /total
@router.message(Command('total'))
async def total_command(message: Message, bot: Bot):
    payload = {"chat_id": message.chat.id, "command": UserCommand.TOTAL.name}
    producer.send(KafkaTopics.USER_COMMANDS.value, payload)


# Этот хендлер срабатывает на команду /results_by_shop
@router.message(Command('results_by_shop'))
async def results_by_shop_command(message: Message, bot: Bot):
    payload = {"chat_id": message.chat.id, "command": UserCommand.RESULTS_BY_SHOP.name}
    producer.send(KafkaTopics.USER_COMMANDS.value, payload)


# Этот хендлер срабатывает на команду /otrs_stats
@router.message(Command('otrs_stats'))
async def otrs_stats_command(message: Message, bot: Bot):
    payload = {"chat_id": message.chat.id, "command": UserCommand.OTRS_STATS.name}
    logger.success(f"Sending message to topic {KafkaTopics.OTRS_STATS.name}")
    producer.send(KafkaTopics.OTRS_STATS.value, payload)


# Этот хендлер срабатывает на команду /equipment
@router.message(Command('equipment'))
async def equipment_command(message: Message, bot: Bot):
    payload = {"chat_id": message.chat.id, "command": UserCommand.EQUIPMENT.name}
    logger.success(f"Sending message to topic {KafkaTopics.EQUIPMENT.name}")
    producer.send(KafkaTopics.EQUIPMENT.value, payload)
