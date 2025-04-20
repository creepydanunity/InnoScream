from aiogram import Router, types
from app_bot.api.api import get_next_scream, post_scream, get_top_screams
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


@screamRouter.message(Command("feed"))
async def handle_feed(msg: types.Message):
    user_id = str(msg.from_user.id)
    try:
        scream = await get_next_scream(user_id)
        await msg.answer(f"🧠 New scream:\n\n{scream['content']}", reply_markup=reaction_keyboard(scream["scream_id"]))
    except Exception as e:
        await msg.answer("😴 There is no more screams today.")


@screamRouter.message(Command("top"))
async def handle_top(msg: types.Message):
    try:
        top = await get_top_screams()
        posts = top.get("posts", [])
        if not posts:
            await msg.answer("😴 No top screams today.")
            return

        for i, scream in enumerate(posts, start=1):
            content = scream["content"]
            votes = scream["votes"]
            meme_url = scream.get("meme_url")
            caption = (
                f"🔥 <b>Top scream #{i}</b>\n"
                f"🗯️ <i>{content}</i>\n"
                f"👍 <b>{votes}</b> votes"
            )

            if meme_url:
                await msg.answer_photo(
                    photo=meme_url,
                    caption=caption,
                    parse_mode="HTML"
                )
            else:
                await msg.answer(caption, parse_mode="HTML")

    except Exception as e:
        await msg.answer("😴 There was an error getting top screams.")
