from aiogram import Router, types
from app_bot.api.api import react_to_scream
from app_bot.utils import send_next_scream


reactionRouter = Router()


@reactionRouter.callback_query(lambda call: call.data.startswith("react:"))
async def handle_reaction(callback: types.CallbackQuery):
    _, scream_id, emoji = callback.data.split(":")
    user_id = str(callback.from_user.id)

    try:
        await react_to_scream(int(scream_id), emoji, user_id)
        await callback.answer(f"{'Skipped!' if emoji == '❌' else f'{emoji} accepted!'}")
    except Exception:
        await callback.answer("❌ Already reacted!")
        return

    await send_next_scream(user_id, callback.message)


@reactionRouter.callback_query(lambda call: call.data == "exit_feed")
async def handle_exit_feed(callback: types.CallbackQuery):
    await callback.message.edit_text("👋 <i>You’ve exited the scream feed</i>", parse_mode="HTML")
    await callback.answer()