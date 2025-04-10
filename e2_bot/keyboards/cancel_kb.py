from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from e2_bot.lexicon import LEXICON


def create_cancel_kb() -> InlineKeyboardMarkup:
    """
    Функция создает клавиатуру с одной кнопкой "Отмена"
    :return: InlineKeyboardMarkup
    """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.add(InlineKeyboardButton(
        text=LEXICON.get('cancel', 'Отмена'),
        callback_data='cancel'
    ))
    return kb_builder.as_markup()
