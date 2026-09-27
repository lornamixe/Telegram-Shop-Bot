from aiogram import types
from bot.locales.translations import translation
from bot.callbacks.itemcallback import ItemCallBack
from bot.callbacks.purchasecallback import PurchaseCallBack

"""
start
"""
def get_start_menu(language):
    buttons = [
        [types.InlineKeyboardButton(text=translation[language]["start_catalog"], callback_data="catalog")],
        [types.InlineKeyboardButton(text=translation[language]["start_services"], callback_data="service")],
        [types.InlineKeyboardButton(text=translation[language]["start_user"], callback_data="user_info")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

"""
user_data
"""

def get_user_data_menu(language):
    buttons =[
        [types.InlineKeyboardButton(text="⬅️", callback_data="start")]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

"""
catalog/service
"""

def get_items_menu(language,items,item_type):

    buttons = [
        [types.InlineKeyboardButton(text=f"{item_name}",callback_data=ItemCallBack(type=item_type,id=item_id).pack())] for item_name,item_id in items
    ] + [[types.InlineKeyboardButton(text="⬅️", callback_data="start")]]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

"""
item_card
"""

def get_item_card_menu(language,item_cost,item_id,item_type):
    buttons = [
        [types.InlineKeyboardButton(text=translation[language]["purchase"],callback_data=PurchaseCallBack(cost=item_cost,id=item_id).pack())],
        [types.InlineKeyboardButton(text="⬅️",callback_data=item_type)]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)


    return keyboard