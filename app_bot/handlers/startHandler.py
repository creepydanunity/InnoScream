from aiogram import Router, types
from aiogram.filters import Command
from app_bot.logger import logger

startRouter = Router()

@startRouter.message(Command("start"))
async def handle_start(msg: types.Message):
    user_id = str(msg.from_user.id)
    logger.info(f"New user started: {user_id}")
    await msg.answer(
        "🗯️ <b>Welcome to InnoScreamBot</b>\n\n"
        "An anonymous place to let it all out. Here's what you can do:\n\n"
        "<b>😤 /scream [text]</b> — Post your scream anonymously\n"
        "<b>🔥 React to screams</b> — Vote with emojis\n"
        "<b>📊 /my_stats</b> — See your scream count & stress trends\n"
        "<b>🏆 /top</b> — View the top scream of the day (with memes!)\n\n"
        "Let's scream it out. You in?",
        parse_mode="HTML"
    )