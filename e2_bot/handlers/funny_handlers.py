from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from loguru import logger

from e2_bot.configs import load_config
from e2_bot.keyboards import funny_kb

config = load_config('.env')

router = Router()


class FSMSaveFunny(StatesGroup):
    select_type = State()


# Хендлер для сохранения гифок
@router.message(F.animation | F.sticker)
async def handle_animation(message: Message, state: FSMContext, bot: Bot):
    file_id, content_type = "", ""
    if message.content_type == 'sticker':
        file_id = message.sticker.file_id
        content_type = 'sticker'
    elif message.content_type == 'animation':
        file_id = message.animation.file_id
        content_type = 'animation'
    await message.reply("Выберите тип сохранения", reply_markup=funny_kb())
    await state.update_data(file_id=file_id, content_type=content_type)
    await state.set_state(FSMSaveFunny.select_type)


@router.callback_query(StateFilter(FSMSaveFunny.select_type))
async def process_select_type(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    logger.debug(state_data)
    logger.debug(callback.data)
    await callback.message.reply(f"Файл сохранён")
    await state.clear()



    # await bot.send_animation(chat_id=message.chat.id, animation="CgACAgQAAxkBAAILV2f6CeqiIm1nRVQshtrOuszoUWYnAAK2AgACyQsNUyezzCs-co_pNgQ")
    # await bot.send_sticker(chat_id=message.chat.id, sticker="CAACAgIAAxkBAAILSGf6CGhnceMKBC0lIw97BfPQnx4kAAL4JAACrpHASF45skRx5PUtNgQ")
