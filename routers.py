from bot.handlers.start import router as start_router
from bot.database.new_user import router as new_user_router
from bot.handlers.user_info import router as user_info_router


all_routers = [
    start_router,
    new_user_router,
    user_info_router
]