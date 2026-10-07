from aiogram import F,types,Router,Bot
from bot.callbacks.itemeditcallback import ItemEditCallBack
from aiogram.fsm.context import FSMContext
from bot.locales.translations import translation
from bot.database.item_utils import get_item_key,get_item_data,set_item_key
from bot.keyboards.menu import get_admin_editor_category_choice_menu,get_admin_editor_choice_menu,get_admin_editor_main_menu,get_admin_editor_visibility_menu
from bot.states.user_data import Data
import asyncio


router = Router()

@router.callback_query(F.data=="admin_panel_editor")
async def editor_choice(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get("lang")

    keyboard = get_admin_editor_category_choice_menu(language)

    await call.message.edit_text(text=translation[language]["editor_choice"], reply_markup=keyboard)




@router.callback_query(ItemEditCallBack.filter())
async def editor(call: types.CallbackQuery, state: FSMContext, callback_data: ItemEditCallBack):

    await call.answer()

    data = await state.get_data()
    language = data.get("lang")

    item_id,item_type,key,tab = callback_data.id,callback_data.type,callback_data.key, callback_data.tab

    if tab==-1:
        keyboard = get_admin_editor_choice_menu(language,item_id,item_type)

        await call.message.edit_text(text=translation[language]["editor_choice"],reply_markup=keyboard)
        return
    elif tab==0 or tab==1:

        item_lang = "_ru" if tab==0 else "_en"

        if key=="preview":
            item_description, item_name, item_cost = await get_item_data(item_lang[1:],item_type,item_id)

            text = f"{item_name}\n\n{item_description}\n\n{translation[language]['cost']}{item_cost}"

            keyboard = get_admin_editor_main_menu(language,item_id,item_type,tab)

            await call.message.edit_text(text=text,reply_markup=keyboard)
            return

        elif key=="Name":
            item_name = await get_item_key(item_id,item_type,key+item_lang)

            text = f"{translation[language]['title']}: \n{item_name}\n\n{translation[language]['edit_text']}"

            await state.set_state(Data.waiting)
            await state.update_data(waiting_for = "Name"+item_lang)

        elif key=="Description":
            item_description = await get_item_key(item_id,item_type,key+item_lang)

            text = f"{translation[language]['description']}: \n{item_description}\n\n{translation[language]['edit_text']}"

            await state.set_state(Data.waiting)
            await state.update_data(waiting_for = "Description"+item_lang)
        elif key=="Delivery_content":
            delivery_content = await get_item_key(item_id,item_type,key+item_lang)

            text = f"{translation[language]['delivery_content']}: \n{delivery_content}\n\n{translation[language]['edit_text']}"

            await state.set_state(Data.waiting)
            await state.update_data(waiting_for = "Delivery_content"+item_lang)
        elif key=="Cost":
            item_cost = await get_item_key(item_id,item_type,key)

            text = f"{translation[language]['cost']}{item_cost}: \n\n{translation[language]['edit_text']}"

            await state.set_state(Data.waiting)
            await state.update_data(waiting_for = "Cost")
    elif tab==2:

        if key in ["Is_hidden","Hide_after_sale"]:

            await set_item_key(item_id,item_type,key,0)

        hide_after_sale = await get_item_key(item_id,item_type,"Hide_after_sale")
        is_hidden = await get_item_key(item_id,item_type,"Is_hidden")


        keyboard = get_admin_editor_visibility_menu(language,item_id,item_type,tab,hide_after_sale,is_hidden)
        text = '123'


        await call.message.edit_text(text=text,reply_markup=keyboard)
        return

    await state.update_data(edit_data = [call.message.message_id,item_id,item_type])

    await call.message.edit_text(text=text,reply_markup=call.message.reply_markup)


@router.message(Data.waiting, F.text)
async def edit_data(message: types.Message, state: FSMContext, bot: Bot):

    data = await state.get_data()
    tab = data.get("waiting_for")
    message_id,item_id,item_type = data.get("edit_data")
    language = data.get("lang")

    await message.delete()

    if tab=="Cost":
        if not message.text.isdecimal():

            msg = await bot.send_message(chat_id=message.chat.id,text=translation[language]["not_numeric"])

            await asyncio.sleep(4)
            await msg.delete()
            return
    elif tab in ["Name_ru","Name_en"]:
        if len(message.text)>14:
            msg = await bot.send_message(chat_id=message.chat.id, text=translation[language]["title_error"])

            await asyncio.sleep(4)
            await msg.delete()
            return
    elif tab in ["Description_en","Description_ru"]:
        if len(message.text)>254:
            msg = await bot.send_message(chat_id=message.chat.id, text=translation[language]["description_error"])

            await asyncio.sleep(4)
            await msg.delete()
            return
    await state.clear()
    await set_item_key(item_id,item_type,tab,message.text)
