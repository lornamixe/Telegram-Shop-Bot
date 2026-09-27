from aiogram import types
from bot.locales.translations import translation

"""
start
"""
def get_start_menu(language):
    buttons = [
        [types.InlineKeyboardButton(text=translation[language]["start_catalog"], callback_data="catalog")],
        [types.InlineKeyboardButton(text=translation[language]["start_services"], callback_data="services")],
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