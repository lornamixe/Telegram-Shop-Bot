import aiosqlite
from config import DB_PATH




async def save_sale(charge_id, amount, item_id, user_id,item_type):

    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()

        await cursor.execute("INSERT OR IGNORE INTO Sales(Charge_id, Amount, Item_id, Item_type, User_id, Status) VALUES (?,?,?,?,?)",(charge_id,amount,item_id,item_type,user_id,1))

        await conn.commit()


async def get_purchased_list(admin, user_id):


    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()

        if admin:

            await cursor.execute("SELECT Date, Id FROM Sales")

        else:

            await cursor.execute("SELECT Date, Id FROM Sales WHERE User_id = ?",(user_id,))

        data = await cursor.fetchall()

        return [x for x in data]

async def get_puchased_info(sale_id):

    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()

        await cursor.execute("SELECT * FROM Sales WHERE Id = ?", (sale_id,))

        data = await cursor.fetchall()

        return [x for x in data[0]]

async def get_info_for_refund(sale_id):

    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()

        await cursor.execute("SELECT Charge_id, User_id FROM Sales WHERE Id = ?", (sale_id,))

        data = await cursor.fetchall()

        return [x for x in data[0]]

async def set_refunded_status(sale_id):

    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()

        await cursor.execute("UPDATE Sales SET Status = 1 WHERE Id = ?",(sale_id,))

        await conn.commit()

