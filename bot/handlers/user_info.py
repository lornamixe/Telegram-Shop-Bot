from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from bot.keyboards.menu import get_back_to_start_menu
from bot.locales.translations import translation
from bot.database.db_utils import get_info


router = Router()

@router.callback_query(F.data=="user_info")
async def user_info(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    language = data.get("lang")

    keyboard = get_back_to_start_menu()

    user_data = await get_info(call.from_user.id)

    await call.message.edit_text(text=translation[language]["user_info"].format(Language = language, Date = user_data[0]),reply_markup=keyboard,parse_mode="HTML")