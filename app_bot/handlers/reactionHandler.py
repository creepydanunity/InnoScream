from aiogram import Router, types
from app_bot.api.api import react_to_scream


reactionRouter = Router()


@reactionRouter.callback_query(lambda call: call.data.startswith("react:"))
async def handle_reaction(callback: types.CallbackQuery):
    _, scream_id, emoji = callback.data.split(":")
    user_id = str(callback.from_user.id)

    try:
        await react_to_scream(int(scream_id), emoji, user_id)
        await callback.answer(f"{emoji} accepted!")
    except Exception as e:
        await callback.answer("❌ Already reacted!")