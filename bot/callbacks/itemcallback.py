from aiogram.filters.callback_data import CallbackData


class ItemCallBack(CallbackData, prefix = "item"):
    type: str
    id: int