from aiogram.filters.callback_data import CallbackData

class ItemEditCallBack(CallbackData, prefix="edit"):
    id: int
    type: str
    key: str
    tab: int