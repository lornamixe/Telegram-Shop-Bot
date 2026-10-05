from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.database.user_utils import save


router = Router()

@router.callback_query(F.data.in_(["ru","en"]))
async def set_lang(call: types.CallbackQuery, state: FSMContext):
    from bot.handlers.start import call_start

    language = str(call.data)


    await state.update_data(lang = language)

    await save(call.from_user.id,language)

    await call_start(call,state)