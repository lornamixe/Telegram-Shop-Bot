from bot.handlers.start import router as start_router
from bot.database.new_user import router as new_user_router
from bot.handlers.user_info import router as user_info_router
from bot.handlers.catalog import router as catalog_router
from bot.handlers.item_data import router as item_data_router
from bot.handlers.service import router as service_router

all_routers = [
    start_router,
    new_user_router,
    user_info_router,
    catalog_router,
    item_data_router,
    service_router
]