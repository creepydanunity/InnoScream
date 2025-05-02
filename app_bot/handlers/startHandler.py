from aiogram import Router, types
from aiogram.filters import Command
from app_bot.logger import logger

startRouter = Router()

@startRouter.message(Command("start"))
async def handle_start(msg: types.Message):
    """
    Handle the /start command to greet new users and introduce bot features.

    Args:
        msg (types.Message): Telegram message that triggered the /start command.

    Behavior:
        - Logs the new user ID.
        - Sends a welcome message explaining the bot's purpose and available commands.
    """
    
    user_id = str(msg.from_user.id)
    logger.info(f"New user started: {user_id}")
    await msg.answer(
        "🗯️ <b>Welcome to InnoScreamBot</b>\n\n"
        "An anonymous place to let it all out. Here's what you can do:\n\n"
        "<b>😤 /scream [text]</b> — Post your scream anonymously\n"
        "<b>🔥 React to screams</b> — Vote with emojis\n"
        "<b>📊 /stats</b> — See your scream & reactions count\n"
        "<b>📈 /stress</b> — View weekly stress graphs\n"
        "<b>📚 /history</b> — Browse top screams from past weeks\n"
        "<b>🏆 /top</b> — View the top scream of the day (with memes!)\n\n"
        "Let's scream it out. You in?",
        parse_mode="HTML"
    )