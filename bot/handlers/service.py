from aiogram.fsm.context import FSMContext
from aiogram import F,types,Router
from bot.database.db_utils import get_items
from bot.locales.translations import translation
from bot.keyboards.menu import get_items_menu

router = Router()

@router.callback_query(F.data == "service")
async def service(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    language = data.get("lang")

    services = await get_items(language,"service")

    await call.message.edit_text(text=translation[language]["service"],reply_markup=get_items_menu(language,services,"service"))