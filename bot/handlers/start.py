from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.locales.translations import translation
from bot.services.find_language import find_language
from bot.services.menu import get_start_menu


router = Router()






@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):

    language = await find_language(message,state)
    if language:
        await message.bot.send_message(text=translation[language]["start"], reply_markup=get_start_menu(language),
                                   chat_id=message.chat.id)

@router.callback_query(F.data=="start")
async def call_start(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()

    language = data.get("lang")

    await call.message.edit_text(text=translation[language]["start"], reply_markup=get_start_menu(language))
    