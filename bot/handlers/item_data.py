from aiogram import F,types,Router
from aiogram.fsm.context import FSMContext
from bot.callbacks.itemcallback import ItemCallBack
from bot.database.item_utils import get_item_data
from bot.locales.translations import translation
from bot.keyboards.menu import get_item_card_menu
from bot.states.user_data import Data


router = Router()

@router.callback_query(ItemCallBack.filter())
async def show_item_card(call: types.CallbackQuery, state: FSMContext, callback_data: ItemCallBack):

    await state.set_state(Data.payment_message)
    await state.update_data(payment_message = [call.message.message_id,call.message.chat.id])

    data = await state.get_data()

    language = data.get("lang")

    message_text, keyboard = await build_item_card(call, language, callback_data)

    await call.message.edit_text(text=message_text,reply_markup=keyboard)

async def build_item_card(call, language: str, callback_data: ItemCallBack):

    item_type, item_id, item_page = callback_data.type, callback_data.id, callback_data.page

    item_description,item_name,item_cost = await get_item_data(language, item_type, item_id)

    text = f"{item_name}\n\n{item_description}\n\n{translation[language]['cost']}{item_cost}"

    keyboard = await get_item_card_menu(language, item_cost, item_id, item_type, item_name, item_description, item_page,call)

    return text, keyboard





