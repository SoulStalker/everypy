"""
Задача для этого модуля:
1. Получить список групп
2. Получить список пользователей
3. Добавить группу
4. Изменить группу
5. Удалить группу
6. Добавить пользователя
7. Удалить пользователя
8. Изменить пользователя
"""
from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from e2_bot.app.data_access.local_db import WAGroupRepository
from e2_bot.app.data_access.local_db import session_maker
from e2_bot.app.use_cases import AddGroupUseCase, GetGroupUseCase
from e2_bot.keyboards import service_kb
from e2_bot.lexicon import LEXICON

router = Router()


class FSMGetAddGroup(StatesGroup):
    fill_gr_id = State()
    fill_gr_name = State()


@router.message(Command('service'))
async def support_command(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Input group id",
        reply_markup=service_kb()
    )
    await state.set_state(FSMGetAddGroup.fill_gr_id)


# Этот хендлер срабатывает на сообщения в FSM состоянии fill_gr_id
@router.message(StateFilter(FSMGetAddGroup.fill_gr_id))
async def process_add_gr(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(gr_id=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Input group name:",
        reply_markup=service_kb()
    )
    await state.set_state(FSMGetAddGroup.fill_gr_name)


# Этот хендлер срабатывает на сообщения в FSM состоянии fill_gr_id
@router.message(StateFilter(FSMGetAddGroup.fill_gr_name))
async def process_add_gr(message: Message, bot: Bot, session: AsyncSession, state: FSMContext):
    await state.update_data(gr_name=message.text)
    state_data = await state.get_data()
    gr_id, gr_name = state_data['gr_id'], state_data['gr_name']
    repo = WAGroupRepository(session)
    uc = AddGroupUseCase(repo)
    ug = GetGroupUseCase(repo)
    logger.debug(gr_id, gr_name)
    try:
        await uc.execute(gr_id, gr_name)
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text=str(e),
            reply_markup=service_kb()
        )
        await state.clear()
        return
    new_gr = await ug.execute(gr_id)
    logger.debug(str(new_gr))
    await bot.send_message(
        chat_id=message.chat.id,
        text=str(new_gr),
        reply_markup=service_kb()
    )
    await state.clear()


# Этот хендлер срабатывает на кнопку "Отмена" и сбрасывает состояние FSM
@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=LEXICON.get('choose_action', 'Выбери действие'),
        reply_markup=service_kb()
    )
    await state.clear()


async def test():
    async with session_maker() as session:
        repo = WAGroupRepository(session)
        uc = AddGroupUseCase(repo)
        await uc.execute("2134@g.us", "test")
