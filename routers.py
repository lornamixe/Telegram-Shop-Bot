from bot.handlers.start import router as start_router
from bot.handlers.set_lang import router as set_lang_router
from bot.handlers.user_info import router as user_info_router
from bot.handlers.item_data import router as item_data_router
from bot.handlers.items import router as items_router
from bot.handlers.payment import router as payment_router
from bot.handlers.refund import router as refund_router
from bot.handlers.admin.admin_panel import router as admin_panel_router
from bot.handlers.admin.admin_panel_editor import router as admin_panel_editor_router

from bot.middlewares.admin_only import AdminOnlyMiddleware

for r in (admin_panel_router,admin_panel_editor_router,refund_router):
    r.message.middleware(AdminOnlyMiddleware())
    r.callback_query.middleware(AdminOnlyMiddleware())

all_routers = [
    start_router,
    set_lang_router,
    user_info_router,
    item_data_router,
    items_router,
    payment_router,
    refund_router,
    admin_panel_router,
    admin_panel_editor_router
]