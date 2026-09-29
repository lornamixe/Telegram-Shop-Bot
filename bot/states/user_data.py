from aiogram.fsm.state import StatesGroup, State


class Data(StatesGroup):

    lang = State()
    payment_message = State()
    admin = State()
