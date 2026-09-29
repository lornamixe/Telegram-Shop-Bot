from aiogram import BaseMiddleware,Bot,types
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Dict, Any
from bot.database.user_utils import check


class LanguageMiddleware(BaseMiddleware):
    async def __call__(self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]) -> Any:
        state = data["state"]
        fsm_data = await state.get_data()
        bot = data["bot"]
        chat = data.get("event_chat")
        

        if isinstance(event, types.CallbackQuery) and event.data in ("ru", "en"):
            return await handler(event,data)



        if fsm_data.get("lang") is None:
            language = await check(event.from_user.id)
            if language:
                await state.update_data(lang=language)
            else:
                buttons = [
                    [types.InlineKeyboardButton(text="🇷🇺 Russian", callback_data="ru")],
                    [types.InlineKeyboardButton(text="🇬🇧 English", callback_data="en")]
                ]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

                await bot.send_message(text="Choose language", reply_markup=keyboard, chat_id=chat.id)
                return

        return await handler(event, data)
