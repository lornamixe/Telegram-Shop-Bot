from aiogram import F,types,Router
from aiogram.fsm.context import FSMContext
from bot.callbacks.itemcallback import ItemCallBack
from bot.database.db_utils import get_item_data
from bot.locales.translations import translation
from bot.keyboards.menu import get_item_card_menu

router = Router()

@router.callback_query(ItemCallBack.filter())
async def show_item_card(call: types.CallbackQuery, state: FSMContext, callback_data: ItemCallBack):

    data = await state.get_data()

    language = data.get("lang")

    item_description,item_name,item_cost = await get_item_data(language,callback_data.type,callback_data.id)



    await call.message.edit_text(text=item_name+'\n\n'+item_description+'\n\n'+translation[language]["cost"]+str(item_cost)+"$",reply_markup=get_item_card_menu(language,item_cost,callback_data.id,callback_data.type))
