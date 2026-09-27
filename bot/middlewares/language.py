from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Dict, Any
from bot.database.new_user import check


class LanguageMiddleware(BaseMiddleware):
    async def __call__(self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]) -> Any:
        state = data["state"]
        fsm_data = await state.get_data()

        if fsm_data.get("lang") is None:
            language = await check(event.from_user.id)
            if language:
                await state.update_data(lang=language)

        return await handler(event, data)
