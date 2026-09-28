import aiosqlite
from config import DB_PATH




async def save_sale(charge_id, amount, item_id, user_id,item_type):

    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()

        await cursor.execute("INSERT INTO Sales(Charge_id, Amount, Item_id, User_id, Item_type) VALUES (?,?,?,?,?)",(charge_id,amount,item_id, user_id,item_type))

        await conn.commit()
