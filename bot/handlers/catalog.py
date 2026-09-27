from aiogram.fsm.context import FSMContext
from aiogram import F,types,Router
from bot.database.db_utils import get_items
from bot.locales.translations import translation
from bot.keyboards.menu import get_items_menu

router = Router()

@router.callback_query(F.data.in_({"catalog","product"}))
async def catalog(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get("lang")

    products = await get_items(language, "product")

    await call.message.edit_text(text=translation[language]["catalog"], reply_markup=get_items_menu(language,products,"product"))

