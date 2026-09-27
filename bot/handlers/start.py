from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.locales.translations import translation
from bot.services.find_language import find_language

router = Router()



def get_main_menu(language):
    buttons = [
        [types.InlineKeyboardButton(text=translation[language]["start_catalog"], callback_data="catalog")],
        [types.InlineKeyboardButton(text=translation[language]["start_services"], callback_data="services")],
        [types.InlineKeyboardButton(text=translation[language]["start_user"], callback_data="user_info")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard







@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):

    language = await find_language(message,state)
    if language:
        await message.bot.send_message(text=translation[language]["start"], reply_markup=get_main_menu(language),
                                   chat_id=message.chat.id)

@router.callback_query(F.data=="start")
async def call_start(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()

    language = data.get("lang")

    await call.message.edit_text(text=translation[language]["start"], reply_markup=get_main_menu(language))
    