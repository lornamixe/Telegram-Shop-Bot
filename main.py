import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot,Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from routers import all_routers
from bot.middlewares.language import LanguageMiddleware

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(*all_routers)

    dp.message.middleware(LanguageMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

