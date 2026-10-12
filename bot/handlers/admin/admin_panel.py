from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from bot.keyboards.menu import get_admin_panel_menu
from bot.locales.translations import translation

router = Router()


@router.callback_query(F.data=="admin_panel")
async def admin_panel(call: types.CallbackQuery, state: FSMContext):
    await call.answer()

    data = await state.get_data()
    language = data.get("lang")

    keyboard = get_admin_panel_menu(language)

    await call.message.edit_text(text=translation[language]["admin_header"], reply_markup=keyboard)