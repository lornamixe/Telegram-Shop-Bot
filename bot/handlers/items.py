from aiogram.fsm.context import FSMContext
from aiogram import F,types,Router
from bot.database.db_utils import get_items
from bot.locales.translations import translation
from bot.keyboards.menu import get_items_menu
from bot.callbacks.pagecallback import PageCallBack

router = Router()

@router.callback_query(PageCallBack.filter())
async def items_list(call: types.CallbackQuery, state: FSMContext, callback_data: PageCallBack):

    data = await state.get_data()
    language = data.get("lang")

    type, page, admin_panel = callback_data.type, callback_data.page, callback_data.admin_panel

    items = await get_items(language,callback_data.type)


    await call.message.edit_text(text = translation[language][type], reply_markup=get_items_menu(language,items,type,page,admin_panel))
