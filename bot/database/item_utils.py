import aiosqlite
from config import DB_PATH

ALLOWED_TABLES = {'product','service'}
ALLOWED_LANGUAGES = {"ru","en"}
ALLOWED_KEYS = {"Id","Cost","Name_ru","Description_ru","Name_en","Description_en","Delivery_content_ru","Delivery_content_en", "Hide_after_sale", "Is_hidden"}




async def get_items(language,item_type, is_admin):

    if language not in ALLOWED_LANGUAGES:
        raise ValueError(f"Invalid language: {language}")

    if item_type not in ALLOWED_TABLES:
        raise ValueError(f"Invalid type: {item_type}")

    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()

        if is_admin:

            await cursor.execute(f"SELECT Name_{language}, Id FROM {item_type.title()} ORDER BY Id")

        else:

            await cursor.execute(f"SELECT Name_{language}, Id FROM {item_type.title()} WHERE Is_hidden == 0 ORDER BY Id")


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


async def get_delivery_content(language,item_id,item_type):

    if item_type not in ALLOWED_TABLES:
        raise ValueError(f"Invalid type: {item_type}")
    if language not in ALLOWED_LANGUAGES:
        raise ValueError(f"Invalid language: {language}")

    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.cursor()

        await cursor.execute(f"SELECT Delivery_content_{language} FROM {item_type.title()} WHERE Id = ?", (item_id,))

        data = await cursor.fetchone()

        return data[0]


async def hide_after_sale(item_id,item_type):

    if item_type not in ALLOWED_TABLES:
        raise ValueError(f"Invalid type: {item_type}")

    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.cursor()

        await cursor.execute(f"UPDATE {item_type.title()} SET Is_hidden = 1 WHERE Id = ? AND Hide_after_sale = 1 ",(item_id,))

        await conn.commit()

async def get_item_key(item_id,item_type,key):

    if item_type not in ALLOWED_TABLES:
        raise ValueError(f"Invalid type: {item_type}")

    if key not in ALLOWED_KEYS:
        raise ValueError(f"Invalid key: {key}")


    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.cursor()

        await cursor.execute(f"SELECT {key} FROM {item_type.title()} WHERE Id = ?",(item_id,))

        data = await cursor.fetchone()


        return data[0]

async def set_item_key(item_id,item_type,key,data):


    if item_type not in ALLOWED_TABLES:
        raise ValueError(f"Invalid type: {item_type}")

    if key not in ALLOWED_KEYS:
        raise ValueError(f"Invalid key: {key}")


    async with aiosqlite.connect(DB_PATH) as conn:

        cursor = await conn.cursor()

        if key in ["Is_hidden","Hide_after_sale"]:
            await cursor.execute(f"UPDATE {item_type.title()} SET {key} = NOT {key} WHERE Id = ?",(item_id,))
        else:
            await cursor.execute(f"UPDATE {item_type.title()} SET {key} = ? WHERE Id = ?", (data,item_id))

        await conn.commit()







