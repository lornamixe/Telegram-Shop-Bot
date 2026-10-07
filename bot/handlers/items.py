from aiogram.fsm.context import FSMContext
from aiogram import F,types,Router
from bot.database.item_utils import get_items
from bot.locales.translations import translation
from bot.keyboards.menu import get_items_menu
from bot.callbacks.pagecallback import PageCallBack
from bot.database.sale_utils import get_purchased_list


router = Router()

@router.callback_query(PageCallBack.filter())
async def items_list(call: types.CallbackQuery, state: FSMContext, callback_data: PageCallBack):
    await call.answer()

    data = await state.get_data()
    language = data.get("lang")

    type, page, admin_edit = callback_data.type, callback_data.page, callback_data.admin_edit

    if type in ["service","product"]:

        items = await get_items(language,callback_data.type,admin_edit)

    else:
        admin = type=="admin_sales"
        items = await get_purchased_list(admin, call.from_user.id)


    await call.message.edit_text(text = translation[language][type], reply_markup=get_items_menu(items,type,page,admin_edit))
