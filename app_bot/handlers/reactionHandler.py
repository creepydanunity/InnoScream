from aiogram import Router, types
from app_bot.api.api import react_to_scream
from app_bot.utils import send_next_scream
from app_bot.logger import logger

reactionRouter = Router()

@reactionRouter.callback_query(lambda call: call.data.startswith("react:"))
async def handle_reaction(callback: types.CallbackQuery):
    try:
        _, scream_id, emoji = callback.data.split(":")
        user_id = str(callback.from_user.id)
        logger.debug(f"User {user_id} reacting with {emoji} to scream {scream_id}")

        await react_to_scream(int(scream_id), emoji, user_id)
        await callback.answer(f"{'Skipped!' if emoji == '❌' else f'{emoji} accepted!'}")
        logger.info(f"Reaction {emoji} recorded for scream {scream_id}")

        await send_next_scream(user_id, callback.message)
    except Exception as e:
        logger.error(f"Reaction failed: {str(e)}", exc_info=True)
        await callback.answer("❌ Already reacted!")

@reactionRouter.callback_query(lambda call: call.data == "exit_feed")
async def handle_exit_feed(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    logger.info(f"User {user_id} exited feed")
    await callback.message.edit_text("👋 <i>You've exited the scream feed</i>", parse_mode="HTML")
    await callback.answer()