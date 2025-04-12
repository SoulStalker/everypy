from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from loguru import logger

from e2_bot.app.data_access.local_db.repository import FunDataRepository
from e2_bot.app.use_cases.funny import AddFunDataUseCase, GetRandomFunnyUseCase
from e2_bot.configs import load_config
from e2_bot.filtes import IsGroupAdmin
from e2_bot.keyboards import funny_kb

config = load_config('.env')

router = Router()


class FSMSaveFunny(StatesGroup):
    select_type = State()


# Хендлер для сохранения гифок
@router.message((F.animation | F.sticker), F.chat.type == 'private')
async def handle_animation(message: Message, state: FSMContext, bot: Bot):
    if message.from_user.id != config.tg_bot.owner_id:
        return
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


@router.callback_query(StateFilter(FSMSaveFunny.select_type), IsGroupAdmin())
async def process_select_type(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    state_data = await state.get_data()
    logger.debug(state_data)
    logger.debug(callback.data)
    uc = AddFunDataUseCase(FunDataRepository(session))
    _, err = await uc.execute(file_id=state_data['file_id'], content_type=state_data['content_type'], answer=callback.data)
    if err:
        await callback.message.reply(err)
        await state.clear()
        return
    await callback.message.reply(f"Файл сохранён")
    await state.clear()
