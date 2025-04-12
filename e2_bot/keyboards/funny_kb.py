from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from e2_bot.lexicon import LEXICON


def funny_kb(width: int = 2) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON.get("good_boy", "Гифка"),
            callback_data='good_boy'
        ),
        InlineKeyboardButton(
            text=LEXICON.get("bad_boy", "Стикер"),
            callback_data='bad_boy'
        ),
    ),
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON.get("all_closed", "Все закрыто"),
            callback_data='all_closed'
        ),
        InlineKeyboardButton(
            text=LEXICON.get("yes_sir", "Будет сделано"),
            callback_data='yes_sir'
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
