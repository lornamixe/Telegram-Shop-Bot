from aiogram.filters.callback_data import CallbackData

class ItemEdit(CallbackData, prefix="edit"):
    id: int
    type: str