from aiogram import Router, types
from app_bot.api.api import get_next_scream, post_scream
from app_bot.keyboards.baseKeyboards import reaction_keyboard
from aiogram.filters import Command


screamRouter = Router()

@screamRouter.message(Command("scream"))
async def handle_scream(msg: types.Message):
    user_id = str(msg.from_user.id)
    content = msg.text.replace("/scream", "").strip()
    
    if not content:
        await msg.reply("😶 What to you want to scream?")
        return

    result = await post_scream(content, user_id)
    scream_id = result["scream_id"]

    await msg.answer(f"😤 Scream accepted:\n\n{content}", reply_markup=reaction_keyboard(scream_id))


@screamRouter.message(Command("next"))
async def handle_next(msg: types.Message):
    user_id = str(msg.from_user.id)
    try:
        scream = await get_next_scream(user_id)
        await msg.answer(f"🧠 New scream:\n\n{scream['content']}", reply_markup=reaction_keyboard(scream["scream_id"]))
    except Exception as e:
        await msg.answer("😴 There is no more screams today.")