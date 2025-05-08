# Third-party
from aiogram import Router, types

# Local application
from app_bot.api.api import react_to_scream
from app_bot.logger import logger
from app_bot.utils import send_next_scream


reactionRouter = Router()


@reactionRouter.callback_query(lambda call: call.data.startswith("react:"))
async def handle_reaction(callback: types.CallbackQuery):
    """
    Handle user reactions to screams via inline button callbacks.

    Args:
        callback (types.CallbackQuery): Callback query with reaction data.

    Behavior:
        - Parses scream ID and emoji from callback data
        - Sends reaction to backend API
        - Acknowledges user with confirmation message
        - Loads next scream after successful reaction
        - Handles already reacted case
    """
    _, scream_id, emoji = callback.data.split(":")
    user_id = str(callback.from_user.id)

    try:
        logger.debug(
            f"User {user_id} reacting with {emoji} "
            f"to scream {scream_id}"
        )

        await react_to_scream(int(scream_id), emoji, user_id)
        response_msg = (
            "Skipped!" if emoji == '❌'
            else f"{emoji} accepted!"
        )
        await callback.answer(response_msg)
        logger.info(f"Reaction {emoji} recorded for scream {scream_id}")

        await send_next_scream(user_id, callback.message)
    except Exception as e:
        logger.error(f"Reaction failed: {str(e)}", exc_info=True)
        await callback.answer("❌ Already reacted!")


@reactionRouter.callback_query(lambda call: call.data == "exit_feed")
async def handle_exit_feed(callback: types.CallbackQuery):
    """
    Handle exit action from scream feed.

    Args:
        callback (types.CallbackQuery): Callback signaling exit action.

    Behavior:
        - Edits message to show exit confirmation
    """
    user_id = str(callback.from_user.id)
    logger.info(f"User {user_id} exited feed")
    await callback.message.edit_text(
        "👋 <i>You've exited the scream feed</i>",
        parse_mode="HTML"
    )
    await callback.answer()
