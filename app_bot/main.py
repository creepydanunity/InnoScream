import os
import asyncio
from aiogram import Bot, Dispatcher
from app_bot.handlers.reactionHandler import reactionRouter
from app_bot.handlers.statsHandler import statsRouter
from app_bot.handlers.screamHandler import screamRouter


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(reactionRouter)
    dp.include_router(screamRouter)
    dp.include_router(statsRouter)

    await dp.start_polling(bot, polling_timeout=120, skip_updates=False)

if __name__ == "__main__":
    asyncio.run(main())


