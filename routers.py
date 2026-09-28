from bot.handlers.start import router as start_router
from bot.handlers.set_lang import router as set_lang_router
from bot.handlers.user_info import router as user_info_router
from bot.handlers.item_data import router as item_data_router
from bot.handlers.items import router as items_router
from bot.handlers.payment import router as payment_router

all_routers = [
    start_router,
    set_lang_router,
    user_info_router,
    item_data_router,
    items_router,
    payment_router
]