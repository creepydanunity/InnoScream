# Third‑party
from aiogram import Router, types
from aiogram.filters import Command

# Local application
from app_bot.api.api import get_my_id
from app_bot.logger import logger


idRouter = Router()

@idRouter.message(Command("my_id"))
async def handle_my_id(msg: types.Message):

    """
    Handles the '/my_id' command to retrieve and send the user's ID.

    When the user sends the '/my_id' command, the bot will:
    - Extract the user ID from the message.
    - Call the `get_my_id` function to retrieve the user ID from the API.
    - Respond with the retrieved user ID if successful.
    - If there is an error, respond with a failure message.

    Args:
        msg (types.Message): The message object containing the user's message and information.

    Returns:
        None
    """

    user_id = str(msg.from_user.id) 

    try:
        logger.debug(f"Getting ID for user {user_id}")
        result = await get_my_id(user_id=user_id)
        await msg.answer(f"Your user_id: {result['user_id']}")
        logger.info(f"ID returned for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to get user_id: {str(e)}", exc_info=True)
        await msg.answer("Failed to get user_id")