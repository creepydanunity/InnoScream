import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher
from handlers import reactionRouter, screamRouter, statsRouter


load_dotenv("app_bot/.env")


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(reactionRouter)
    dp.include_router(screamRouter)
    dp.include_router(statsRouter)

    await dp.start_polling(bot, polling_timeout=120, skip_updates=False)

if __name__ == "__main__":
    asyncio.run(main())


