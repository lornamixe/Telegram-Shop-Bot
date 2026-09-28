from bot.database.user_utils import check
from bot.states.user_data import Data
from aiogram.fsm.context import FSMContext
from aiogram import types


async def find_language(message: types.Message, state: FSMContext):

    data = await state.get_data()
    if data.get("lang") is None:
        language = await check(message.from_user.id)

        if not language:
            buttons = [
                [types.InlineKeyboardButton(text="🇷🇺 Russian", callback_data="ru")],
                [types.InlineKeyboardButton(text="🇬🇧 English", callback_data="en")]
            ]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

            await message.bot.send_message(text="Choose language", reply_markup=keyboard, chat_id=message.chat.id)
            return

        else:
            await state.set_state(Data.lang)
            await state.update_data(lang=language)
    else:
        language = data.get("lang")

    return language