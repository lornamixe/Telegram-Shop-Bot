from aiogram import types
from bot.locales.translations import translation
from bot.callbacks.itemcallback import ItemCallBack
from bot.callbacks.purchasecallback import PurchaseCallBack
from bot.callbacks.pagecallback import PageCallBack
from math import floor
from bot.callbacks.refundcallback import RefundCallBack
from bot.callbacks.itemeditcallback import ItemEditCallBack

"""
start
"""
def get_start_menu(language,admin):
    buttons = [
        [types.InlineKeyboardButton(text=translation[language]["catalog"], callback_data=PageCallBack(type="product",page=0,admin_edit=False).pack())],
        [types.InlineKeyboardButton(text=translation[language]["services"], callback_data=PageCallBack(type="service",page=0,admin_edit=False).pack())],
        [types.InlineKeyboardButton(text=translation[language]["user_sales"],callback_data=PageCallBack(type="user_sales",page=0,admin_edit=False).pack())],
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



    if not admin_panel:
        # Adding a list of items in current page.
        buttons = [[types.InlineKeyboardButton(text=f"{item_name}",callback_data=ItemCallBack(page=page,type=item_type,id=item_id).pack())] for item_name, item_id in items_list]
    else:
        buttons = [[types.InlineKeyboardButton(text=f"{item_name}", callback_data=ItemEditCallBack(id=item_id,tab=-1,key="None",type=item_type,language="None").pack())] for item_name, item_id in items_list]
    page_button = [[]]

    if n>5:
        if page>0:
            page_button[0].append(types.InlineKeyboardButton(text="⬅️",callback_data=PageCallBack(page=(page-1),type=item_type,admin_edit=admin_panel).pack())) # to prevent navigating to a negative page number
        if k>page:
            page_button[0].append(types.InlineKeyboardButton(text="➡️",callback_data=PageCallBack(page=(page+1),type=item_type,admin_edit=admin_panel).pack())) # to prevent navigating beyond the last page

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
        [types.InlineKeyboardButton(text="⬅️",callback_data=PageCallBack(page=page,type=item_type,admin_edit=False).pack())]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)


    return keyboard


"""
sold_item_card
"""

def get_sold_item_card_menu(language, admin, id, page,status):

    buttons = []

    if admin:

        if status == 0:

            buttons = [
                [types.InlineKeyboardButton(text=translation[language]["refund"], callback_data=RefundCallBack(id=id,page=page).pack())],
            ]

        buttons.append([types.InlineKeyboardButton(text="⬅️",callback_data=PageCallBack(page=page, type="admin_sales",admin_edit=False).pack())])

    else:
        buttons.append([types.InlineKeyboardButton(text="⬅️",callback_data=PageCallBack(page=page, type="user_sales",admin_edit=False).pack())])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


"""
admin_panel
"""

def get_admin_panel_menu(language):

    buttons = [
        [types.InlineKeyboardButton(text=translation[language]["editor"],callback_data="admin_panel_editor")],
        [types.InlineKeyboardButton(text=translation[language]["sales"], callback_data=PageCallBack(page=0,type="admin_sales",admin_edit=False).pack())],
        [types.InlineKeyboardButton(text="⬅️",callback_data="start")]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


def get_admin_editor_category_choice_menu(language):

    buttons = [
        [types.InlineKeyboardButton(text=translation[language]["catalog"], callback_data=PageCallBack(page=0,type="product",admin_edit = True).pack())],
        [types.InlineKeyboardButton(text=translation[language]["services"],callback_data=PageCallBack(page=0, type="service", admin_edit=True).pack())],
        [types.InlineKeyboardButton(text="⬅️",callback_data="admin_panel")]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard


def get_admin_editor_choice_menu(language,item_id,item_type):

    buttons = [
        [types.InlineKeyboardButton(text=translation[language]["russian"], callback_data=ItemEditCallBack(tab=0,key="preview",id=item_id,type=item_type,language="ru").pack())],
        [types.InlineKeyboardButton(text=translation[language]["english"], callback_data=ItemEditCallBack(tab=1,key="preview",id=item_id,type=item_type,language="en").pack())],
        [types.InlineKeyboardButton(text=translation[language]["visibility"], callback_data=ItemEditCallBack(tab=2,key="preview",id=item_id,type=item_type,language="None").pack())],
        [types.InlineKeyboardButton(text="⬅️",callback_data=PageCallBack(page=0, type=item_type, admin_edit=True).pack())]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_admin_editor_main_menu(language,item_id,item_type,tab):

    buttons = [
        [types.InlineKeyboardButton(text=translation[language]["preview"],callback_data=ItemEditCallBack(tab=tab,key="preview",id=item_id,type=item_type).pack())],
        [types.InlineKeyboardButton(text=translation[language]["title"],callback_data=ItemEditCallBack(tab=tab, key=f"Name",id=item_id,type=item_type).pack()),
         types.InlineKeyboardButton(text=translation[language]["description"], callback_data=ItemEditCallBack(tab=tab, key=f"Description",id=item_id,type=item_type).pack()),
         types.InlineKeyboardButton(text=translation[language]["delivery_content"], callback_data=ItemEditCallBack(tab=tab, key=f"Delivery_content",id=item_id,type=item_type).pack())],
        [types.InlineKeyboardButton(text=translation[language]["cost"], callback_data=ItemEditCallBack(tab=tab, key=f"Cost",id=item_id,type=item_type).pack())],
        [types.InlineKeyboardButton(text="⬅️",callback_data=ItemEditCallBack(id=item_id,tab=-1,key="None",type=item_type).pack())]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

def get_admin_editor_visibility_menu(language,item_id,item_type,tab,hide_after_sale,is_hidden):

    hidden = "🟢" if is_hidden else "🔴"
    hide = "🟢" if hide_after_sale else "🔴"


    buttons = [
        [types.InlineKeyboardButton(text=f"{hidden} {translation[language]['is_hidden']}",callback_data=ItemEditCallBack(tab=tab,key="Is_hidden",id=item_id,type=item_type).pack())],
        [types.InlineKeyboardButton(text=f"{hide} {translation[language]['hide_after_sale']}",callback_data=ItemEditCallBack(tab=tab,key="Hide_after_sale",id=item_id,type=item_type).pack())],
        [types.InlineKeyboardButton(text="⬅️", callback_data=ItemEditCallBack(id=item_id, tab=-1, key="None",type=item_type).pack())]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard