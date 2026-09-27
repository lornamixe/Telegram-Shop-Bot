from bot.handlers.start import router as start_router
from bot.database.new_user import router as new_user_router



all_routers = [
    start_router,
    new_user_router
]