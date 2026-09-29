from aiogram import types
from bot.locales.translations import translation
from bot.callbacks.itemcallback import ItemCallBack
from bot.callbacks.purchasecallback import PurchaseCallBack
from bot.callbacks.pagecallback import PageCallBack
from math import floor

"""
start
"""
def get_start_menu(language,admin):
    buttons = [
        [types.InlineKeyboardButton(text=translation[language]["start_catalog"], callback_data=PageCallBack(type="product",page=0,admin_panel=False).pack())],
        [types.InlineKeyboardButton(text=translation[language]["start_services"], callback_data=PageCallBack(type="service",page=0,admin_panel=False).pack())],
        [types.InlineKeyboardButton(text=translation[language]["start_user"], callback_data="user_info")]
    ]

    if admin:
        buttons += [[types.InlineKeyboardButton(text=translation[language]["admin"], callback_data = "admin_panel")]]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

"""
back to start (user_data,top_up)
"""

def get_back_to_start_menu():
    buttons =[
        [types.InlineKeyboardButton(text="🏠", callback_data="start")]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

"""
catalog/service
"""

def get_items_menu(items,item_type,page,admin_panel):



    items_list = [x for idx,x in enumerate(items) if page*5<=idx<(page+1)*5]

    n = len(items)
    k = floor(n/5)



    # Adding a list of items in current page.
    buttons = [[types.InlineKeyboardButton(text=f"{item_name}",callback_data=ItemCallBack(page=page,type=item_type,id=item_id).pack())] for item_name, item_id in items_list]

    page_button = [[]]

    if n>5:
        if page>0:
            page_button[0].append(types.InlineKeyboardButton(text="⬅️",callback_data=PageCallBack(page=(page-1),type=item_type,admin_panel=admin_panel).pack())) # to prevent navigating to a negative page number
        if k>page:
            page_button[0].append(types.InlineKeyboardButton(text="➡️",callback_data=PageCallBack(page=(page+1),type=item_type,admin_panel=admin_panel).pack())) # to prevent navigating beyond the last page

    if page_button[0]:
        buttons+=page_button

    buttons += [[types.InlineKeyboardButton(text="🏠︎",callback_data="start")]] # return to start button

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

"""
item_card
"""

async def get_item_card_menu(language,item_cost,item_id,item_type,item_name,item_description,page,call):

    purchase_link = await call.bot.create_invoice_link(
        title=item_name,
        description=item_description,
        payload=f"{item_id}:{call.from_user.id}:{item_type}",
        currency="XTR",
        prices=[types.LabeledPrice(label=item_name,amount=item_cost)],
        provider_token="",
    )



    buttons = [
        [types.InlineKeyboardButton(text=translation[language]["purchase"]+str(item_cost)+"⭐️",url=purchase_link)],
        [types.InlineKeyboardButton(text="⬅️",callback_data=PageCallBack(page=page,type=item_type,admin_panel=False).pack())]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)


    return keyboard