from aiogram import Router, types
from app_bot.api.api import post_scream, get_top_screams
from aiogram.filters import Command
from app_bot.utils import send_next_scream


screamRouter = Router()

@screamRouter.message(Command("scream"))
async def handle_scream(msg: types.Message):
    user_id = str(msg.from_user.id)
    content = msg.text.replace("/scream", "").strip()
    
    if not content:
        await msg.reply("😶 <i>What do you want to scream?</i>", parse_mode="HTML")
        return

    result = await post_scream(content, user_id)
    scream_id = result["scream_id"]

    await msg.answer("😤 <b>Your scream has been unleashed into the void!</b>", parse_mode="HTML")


@screamRouter.message(Command("feed"))
async def handle_feed(msg: types.Message):
    """
    Handle the /feed command to display the next unseen scream to the user.

    Args:
        msg (types.Message): Incoming Telegram message containing the /feed command.

    Behavior:
        - Sends a temporary loading message to the user.
        - Delegates the actual scream retrieval and delivery to `send_next_scream()`,
          passing the user's Telegram ID and the loading message for context.
    """
    
    dummy_msg = await msg.answer("⏳ Loading your scream...")
    await send_next_scream(str(msg.from_user.id), dummy_msg)


@screamRouter.message(Command("top"))
async def handle_top(msg: types.Message):
    """
    Handle the /top command to display today's top screams.

    Args:
        msg (types.Message): Incoming Telegram message containing the /top command.

    Behavior:
        - Fetches the top screams from the backend.
        - Sends each top scream to the chat with its content, vote count, and meme image (if available).
        - If there are no top screams, informs the user.
        - If an error occurs, notifies the user about the failure.
    """
    try:
        top = await get_top_screams()
        posts = top.get("posts", [])
        if not posts:
            await msg.answer("😴 No top screams today...")
            return

        for i, scream in enumerate(posts, start=1):
            content = scream["content"]
            votes = scream["votes"]
            meme_url = scream.get("meme_url")
            caption = (
                f"🔥 <b>Top scream #{i}</b>\n"
                f"🗯️ <i>{content}</i>\n"
                f"👍 <b>{votes}</b> {'vote' if votes == 1 else 'votes'}"
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
        await msg.answer("😴 There was an error getting top screams((")
