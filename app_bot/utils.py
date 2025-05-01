from aiogram import types
from app_bot.api.api import get_next_scream
from app_bot.keyboards.baseKeyboards import reaction_keyboard
from app_bot.logger import logger

async def send_next_scream(user_id: str, message: types.Message):
    """
    Edit a message to display the next unseen scream for the user.

    Args:
        user_id (str): The Telegram user's ID.
        message (types.Message): The Telegram message to edit with the next scream content.

    Behavior:
        - Retrieves the next unseen scream via the backend API.
        - Edits the given message to display the scream content with inline reaction buttons.
        - If no screams are available or an error occurs, shows a fallback message.
    """

    try:
        logger.debug(f"Sending next scream for user {user_id}")
        scream = await get_next_scream(user_id)
        caption = (
            f"😱 <b>New scream:</b>\n\n"
            f"🗯️ <i>{scream['content']}</i>"
        )
        await message.edit_text(
            caption,
            reply_markup=reaction_keyboard(scream["scream_id"]),
            parse_mode="HTML"
        )
        logger.info(f"Scream {scream['scream_id']} sent to user {user_id}")
    except Exception as e:
        logger.warning(f"No screams available for user {user_id}: {str(e)}")
        await message.edit_text("😴 <i>No more screams in the feed for now...</i>", parse_mode="HTML")