import aiosqlite
from config import DB_PATH

ALLOWED_TABLES = {'product','service'}
ALLOWED_LANGUAGES = {"ru","en"}





async def get_items(language,item_type):

    if language not in ALLOWED_LANGUAGES:
        raise ValueError(f"Invalid language: {language}")

    if item_type not in ALLOWED_TABLES:
        raise ValueError(f"Invalid type: {item_type}")

    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()

        await cursor.execute(f"SELECT Name_{language}, Id FROM {item_type.title()} ORDER BY Id")


        data = await cursor.fetchall()

        return [x for x in data]

async def get_item_data(language,item_type,item_id):

    if language not in ALLOWED_LANGUAGES:
        raise ValueError(f"Invalid language: {language}")

    if item_type not in ALLOWED_TABLES:
        raise ValueError(f"Invalid type: {item_type}")


    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()

        await cursor.execute(f"SELECT Description_{language}, Name_{language}, Cost FROM {item_type.title()} WHERE Id = ?",(item_id,))

        data = await cursor.fetchall()

        return [x for x in data[0]]


async def get_after_payment_data(item_id,item_type):

    if item_type not in ALLOWED_TABLES:
        raise ValueError(f"Invalid type: {item_type}")

    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.cursor()

        await cursor.execute(f"SELECT After_payment FROM {item_type.title()} WHERE Id = ?", (item_id,))

        data = await cursor.fetchone()

        return data[0]