import aiosqlite
from config import DB_PATH

async def get_info(user_id,balance,date):

    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()
        await cursor.execute("SELECT Balance, register_date FROM Users WHERE UserId = ?",(user_id,))

        data = await cursor.fetchone()


        if not balance:
            del data[0]
        if not date:
            del data[1]


        return data