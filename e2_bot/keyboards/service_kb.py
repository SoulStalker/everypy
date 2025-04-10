from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from e2_bot.lexicon import LEXICON


def service_kb(width: int = 2) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON.get("get_groups", "Получить группы"),
            callback_data='get_groups'
        ),
        InlineKeyboardButton(
            text=LEXICON.get("get_contacts", "Получить контакты"),
            callback_data='get_contacts'
        ),
    ),
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON.get("add_group", "Добавить группу"),
            callback_data='add_group'
        ),
        InlineKeyboardButton(
            text=LEXICON.get("add_contact", "Добавить контакт"),
            callback_data='add_contact'
        ),
    ),
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON.get("cancel", "Отменить"),
            callback_data='cancel'
        ),
        width=width
    )
    return kb_builder.as_markup()
