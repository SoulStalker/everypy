from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


# Игнорируем всех кого не знаем
class ShadowBanMiddleware(BaseMiddleware):

    def __init__(self, admins):
        self.admins = admins

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        user: User = data.get('event_from_user')
        if user is not None:
            if user.id not in self.admins:
                return

        return await handler(event, data)
