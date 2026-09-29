from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.locales.translations import translation
from bot.keyboards.menu import get_start_menu
from bot.middlewares.admin import AdminMiddleware

router = Router()

router.message.middleware(AdminMiddleware())
router.callback_query.middleware(AdminMiddleware())




@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):

    data = await state.get_data()

    language = data.get("lang")
    admin = data.get("admin")

    if language:
        await message.bot.send_message(text=translation[language]["start"], reply_markup=get_start_menu(language,admin),
                                   chat_id=message.chat.id)

@router.callback_query(F.data=="start")
async def call_start(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()

    language = data.get("lang")
    admin = data.get("admin")

    await call.message.edit_text(text=translation[language]["start"], reply_markup=get_start_menu(language,admin))
    