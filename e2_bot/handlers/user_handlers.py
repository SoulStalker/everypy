from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from e2_bot.lexicon import LEXICON


router = Router()


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
    pass