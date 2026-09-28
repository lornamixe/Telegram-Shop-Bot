import aiosqlite
from config import DB_PATH



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
        await cursor.execute("INSERT OR IGNORE INTO Users (UserId,Language) VALUES (?,?)", (user_id,language))

        await conn.commit()



async def get_info(user_id):

    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()
        await cursor.execute("SELECT Register_date FROM Users WHERE UserId = ?",(user_id,))

        data = await cursor.fetchall()
        data = [x for x in data[0]]


        return data
