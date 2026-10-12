from aiogram import BaseMiddleware, types
from bot.database.user_utils import get_admin_status

class AdminOnlyMiddleware(BaseMiddleware):
    async def __call__(self,handler,event,data):
        if not await get_admin_status(event.from_user.id):
            if isinstance(event, types.CallbackQuery):
                await event.answer("Access denied", show_alert=True)
            return
        return await handler(event,data)