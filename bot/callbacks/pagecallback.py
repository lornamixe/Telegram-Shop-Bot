from aiogram.filters.callback_data import CallbackData

class PageCallBack(CallbackData, prefix="page"):
    page: int
    type: str
    admin_edit: bool