from aiogram import Router, types
from app_bot.api.api import get_next_scream, react_to_scream
from app_bot.keyboards.baseKeyboards import reaction_keyboard


reactionRouter = Router()


@reactionRouter.callback_query(lambda call: call.data.startswith("react:"))
async def handle_reaction(callback: types.CallbackQuery):
    _, scream_id, emoji = callback.data.split(":")
    user_id = str(callback.from_user.id)

    try:
        await react_to_scream(int(scream_id), emoji, user_id)

        await callback.message.edit_reply_markup(reply_markup=None)
        
        if emoji == "❌":
            await callback.answer(f"Skipped!")
        else:
            await callback.answer(f"{emoji} accepted!")
    except Exception as e:
        await callback.answer("❌ Already reacted!")
    
    try:
        scream = await get_next_scream(user_id)
        await callback.message.answer(
            f"🧠 New scream:\n\n{scream['content']}",
            reply_markup=reaction_keyboard(scream["scream_id"])
        )
    except Exception:
        await callback.message.answer("😴 No more screams left for today.")