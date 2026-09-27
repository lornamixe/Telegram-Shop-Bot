from aiogram.filters.callback_data import CallbackData


class PurchaseCallBack(CallbackData, prefix = "purchase"):
    cost: int
    id: int
