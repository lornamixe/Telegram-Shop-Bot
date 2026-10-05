from aiogram import BaseMiddleware,Bot,types
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Dict, Any
from bot.database.user_utils import get_admin_status


class AdminMiddleware(BaseMiddleware):

    async def __call__(self,
           handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
           event: TelegramObject,
           data: Dict[str, Any]) -> Any:

        state = data["state"]
        fsm_data = await state.get_data()

        if fsm_data.get("admin") is None:
            admin = await get_admin_status(event.from_user.id)

            await state.update_data(admin=admin)

        return await handler(event, data)
