"""
Задача для этого модуля:
1. Получить список групп +
2. Получить список пользователей +
3. Добавить группу +
4. Изменить группу
5. Удалить группу
6. Добавить пользователя +
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

from e2_bot.app.data_access import WAContactRepository
from e2_bot.app.data_access.local_db import WAGroupRepository
from e2_bot.app.data_access.local_db import session_maker
from e2_bot.app.use_cases import AddGroupUseCase, GetModelUseCase, AddContactUseCase
from e2_bot.app.use_cases.wa_groups import GetAllUseCase
from e2_bot.filtes import IsGroupAdmin
from e2_bot.keyboards import service_kb, create_cancel_kb
from e2_bot.lexicon import LEXICON

router = Router()


class FSMGetAddGroup(StatesGroup):
    fill_gr_id = State()
    fill_gr_name = State()
    fill_phone = State()
    fill_name = State()
    fill_last_name = State()
    fill_email = State()
    fill_tg = State()


@router.message(Command('service'))
async def service_command(message: Message, bot: Bot):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Выбери действие:\n",
        reply_markup=service_kb()
    )


@router.callback_query(F.data == 'get_groups')
async def get_groups_command(callback: CallbackQuery, session: AsyncSession):
    groups = await get_content_from_repo(session=session, t=WAGroupRepository)
    try:
        await callback.message.edit_text(
            text="\n".join(groups),
            reply_markup=service_kb()
        )
    except Exception as e:
        logger.error(e)


@router.callback_query(F.data == 'get_contacts')
async def get_contacts_command(callback: CallbackQuery, session: AsyncSession):
    contacts = await get_content_from_repo(session=session, t=WAContactRepository)
    try:
        await callback.message.edit_text(
            text="\n".join(contacts),
            reply_markup=service_kb()
        )
    except Exception as e:
        logger.error(e)


@router.callback_query(F.data == 'add_group', IsGroupAdmin())
async def add_group_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON.get("input_group_id"),
        reply_markup=create_cancel_kb()
    )
    await state.set_state(FSMGetAddGroup.fill_gr_id)


# Этот хендлер срабатывает на сообщения в FSM состоянии fill_gr_id
@router.message(StateFilter(FSMGetAddGroup.fill_gr_id), IsGroupAdmin())
async def process_add_gr(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(gr_id=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=LEXICON.get("input_group_name"),
        reply_markup=create_cancel_kb()
    )
    await state.set_state(FSMGetAddGroup.fill_gr_name)


# Этот хендлер срабатывает на сообщения в FSM состоянии fill_gr_id
@router.message(StateFilter(FSMGetAddGroup.fill_gr_name), IsGroupAdmin())
async def process_fill_gr(message: Message, bot: Bot, session: AsyncSession, state: FSMContext):
    await state.update_data(gr_name=message.text)
    state_data = await state.get_data()
    gr_id, gr_name = state_data['gr_id'], state_data['gr_name']
    new_gr = await add_data_to_repo(session=session, t=WAGroupRepository, group_id=gr_id, group_name=gr_name)
    logger.debug(str(new_gr))
    await bot.send_message(
        chat_id=message.chat.id,
        text=str(new_gr),
        reply_markup=service_kb()
    )
    await state.clear()


@router.callback_query(F.data == 'add_contact', IsGroupAdmin())
async def add_contact_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON.get("input_phone"),
        reply_markup=create_cancel_kb()
    )
    await state.set_state(FSMGetAddGroup.fill_phone)


# Этот хендлер срабатывает на сообщения в FSM состоянии fill_gr_id
@router.message(StateFilter(FSMGetAddGroup.fill_phone), IsGroupAdmin())
async def process_add_ct(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(phone=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=LEXICON.get("input_contact_name"),
        reply_markup=create_cancel_kb()
    )
    await state.set_state(FSMGetAddGroup.fill_name)


# Этот хендлер срабатывает на сообщения в FSM состоянии fill_name
@router.message(StateFilter(FSMGetAddGroup.fill_name), IsGroupAdmin())
async def process_fill_name(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(first_name=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=LEXICON.get('input_contact_last_name'),
        reply_markup=create_cancel_kb()
    )
    await state.set_state(FSMGetAddGroup.fill_last_name)


# Этот хендлер срабатывает на сообщения в FSM состоянии fill_last_name
@router.message(StateFilter(FSMGetAddGroup.fill_last_name), IsGroupAdmin())
async def process_fill_ln(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(last_name=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=LEXICON.get('input_contact_email'),
        reply_markup=create_cancel_kb()
    )
    await state.set_state(FSMGetAddGroup.fill_email)


# Этот хендлер срабатывает на сообщения в FSM состоянии fill_email
@router.message(StateFilter(FSMGetAddGroup.fill_email), IsGroupAdmin())
async def process_fill_email(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(email=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=LEXICON.get('input_contact_tg'),
        reply_markup=create_cancel_kb()
    )
    await state.set_state(FSMGetAddGroup.fill_tg)


# Этот хендлер срабатывает на сообщения в FSM состоянии fill_tg
@router.message(StateFilter(FSMGetAddGroup.fill_tg), IsGroupAdmin())
async def process_fill_tg(message: Message, bot: Bot, session: AsyncSession, state: FSMContext):
    await state.update_data(telegram_id=message.text)
    state_data = await state.get_data()
    phone = state_data['phone']
    first_name = state_data['first_name']
    last_name = state_data['last_name']
    email = state_data['email']
    telegram_id = state_data['telegram_id']
    new_ct = await add_data_to_repo(
        session=session,
        t=WAContactRepository,
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        email=email,
        telegram_id=telegram_id
    )
    logger.debug(str(new_ct))
    await bot.send_message(
        chat_id=message.chat.id,
        text=str(new_ct),
        reply_markup=service_kb()
    )
    await state.clear()


# Этот хендлер срабатывает на кнопку "Отмена" и сбрасывает состояние FSM
@router.callback_query(F.data == 'cancel')
async def process_cancel(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=LEXICON.get('choose_action', 'Выбери действие'),
        reply_markup=service_kb()
    )
    await state.clear()


async def get_content_from_repo(session: AsyncSession, t: type, pk: str = None) -> str:
    repository = t(session)
    if pk:
        uc = GetModelUseCase(repository)
        return await uc.execute(pk)
    else:
        uc = GetAllUseCase(repository)
        result = await uc.execute()
        logger.debug(result)
        return result


async def add_data_to_repo(session: AsyncSession, t: type, **kwargs) -> str:
    uc = None
    repository = t(session)
    logger.debug(repository)
    if type(repository) is WAGroupRepository:
        uc = AddGroupUseCase(repository)
    elif type(repository) is WAContactRepository:
        uc = AddContactUseCase(repository)
    logger.debug(uc)
    if uc:
        try:
            return await uc.execute(**kwargs)
        except Exception as e:
            return str(e)


async def test():
    async with session_maker() as session:
        repo = WAGroupRepository(session)
        uc = AddGroupUseCase(repo)
        await uc.execute("2134@g.us", "test")
