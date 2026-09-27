import aiosqlite
from config import DB_PATH
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.states.user_data import Data



router = Router()

@router.callback_query(F.data.in_(["ru","en"]))
async def set_lang(call: types.CallbackQuery, state: FSMContext):
    from bot.handlers.start import call_start

    language = str(call.data)


    await state.set_state(Data.lang)
    await state.update_data(lang = language)

    await save(call.from_user.id,language)

    await call_start(call,state)



async def check(user_id):
    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()
        await cursor.execute("SELECT Language FROM Users WHERE UserId = ?", (user_id,))

        exists = await cursor.fetchone()

        if exists:
            return exists[0]
        else:
            return

async def save(user_id,language):

    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()
        await cursor.execute("INSERT INTO Users (UserId,Language) VALUES (?,?)", (user_id,language))

        await conn.commit()

