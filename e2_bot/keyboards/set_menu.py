from aiogram import Bot
from aiogram.types import BotCommand

from e2_bot.lexicon import LEXICON_COMMANDS


# Функция для установки главного меню
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description,
        ) for command, description in LEXICON_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu_commands)
