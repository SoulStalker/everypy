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
import asyncio

from e2_bot.app.data_access.local_db import WAGroupRepository
from e2_bot.app.data_access.local_db import session_maker
#
# from datetime import datetime, time, timedelta
#
# from aiogram import F, Router, Bot
# from aiogram.filters import Command, CommandStart, StateFilter
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, CallbackQuery, FSInputFile
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from keyboards.keyboards import (common_keyboard, create_tasks_keyboard, create_add_task_kb,
#                                  create_del_tasks_kb, create_stop_task_kb, create_start_yes_no_kb,
#                                  create_stats_kb, create_cancel_kb, create_del_or_edit_tasks_kb,
#                                  create_edit_tasks_kb, create_service_kb, create_what_to_change_kb)
# from lexicon.lexicon import LEXICON_RU
# from filters.filters import (IsUsersDelTasks, ShowUsersTasks, IsStopTasks, IsInPeriods,
#                              IsUsersEditTasks, IsCorrectSymbols)
# from database.orm_query import (orm_get_user_by_id, orm_add_user, orm_add_task, orm_get_tasks_list,
#                                 orm_remove_task, orm_update_work, orm_stop_work, orm_edit_task,
#                                 orm_get_settings, orm_update_settings, orm_add_default_settings,
#                                 orm_get_unclosed_work, orm_get_last_work, orm_get_task_by_id, orm_get_task_by_name)
# from services.services import orm_get_day_stats
# from bot import FSMGetTaskName
#
# router = Router()
#
#
# # Этот хендлер срабатывает на команду /service
# @router.message(Command('service'))
# async def support_command(message: Message, session: AsyncSession, bot: Bot):
#     user = await orm_get_user_by_id(session, message.from_user.id)
#     current_settings = await orm_get_settings(session, user.id)
#     if current_settings is None:
#         await orm_add_default_settings(session, user.id)
#     await bot.send_message(
#         chat_id=message.chat.id,
#         text=(f"{LEXICON_RU['/service']}{LEXICON_RU['current_work_duration']} "
#               f"{current_settings.work_duration} {LEXICON_RU['minutes']}\n{LEXICON_RU['current_break_duration']} "
#               f"{current_settings.break_duration} {LEXICON_RU['minutes']}"),
#         reply_markup=create_service_kb()
#     )
from e2_bot.app.use_cases import AddGroupUseCase


async def test():
    async with session_maker() as session:
        repo = WAGroupRepository(session)
        uc = AddGroupUseCase(repo)
        await uc.execute("120363417612072620@g.us", "Gophers")


if __name__ == '__main__':
    asyncio.run(test())
