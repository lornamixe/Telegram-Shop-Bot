from aiogram.filters.callback_data import CallbackData

class RefundCallBack(CallbackData, prefix="refund"):
    id: int
    page: int