# Third-party
from aiogram import Router, types
from aiogram.filters import Command

# Local application
from app_bot.api.api import get_top_screams, post_scream
from app_bot.logger import logger
from app_bot.utils import send_next_scream


screamRouter = Router()


@screamRouter.message(Command("scream"))
async def handle_scream(msg: types.Message):
    """
    Handle the /scream command to post a new scream.

    Args:
        msg (types.Message): Telegram message containing the scream text.

    Behavior:
        - Extracts the scream content from the message
        - If empty, prompts user to type something
        - Sends scream to backend API using `post_scream()`
        - Notifies user of success or failure
    """
    user_id = str(msg.from_user.id)
    content = msg.text.replace("/scream", "").strip()
    if not content:
        logger.warning(
            f"Empty scream from user {user_id}"
            )  # pragma: no mutate
        await msg.reply(
            "😶 <i>What do you want to scream?</i>",
            parse_mode="HTML"
        )
        return

    try:
        logger.info(
            f"Processing scream from user {user_id}"
            )  # pragma: no mutate
        result = await post_scream(content, user_id)
        scream_id = result["scream_id"]
        logger.info(
            f"Scream {scream_id} posted by user {user_id}"
            )  # pragma: no mutate
        await msg.answer(
            "😤 <b>Your scream has been unleashed into the void!</b>",
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(
            f"Failed to post scream: {str(e)}", exc_info=True
            )  # pragma: no mutate
        await msg.answer("❌ Failed to post your scream")


@screamRouter.message(Command("feed"))
async def handle_feed(msg: types.Message):
    """
    Handle the /feed command to display next unseen scream.

    Args:
        msg (types.Message): Telegram message with /feed command.

    Behavior:
        - Sends temporary loading message
        - Delegates retrieval to `send_next_scream()`
    """
    user_id = str(msg.from_user.id)
    logger.info(f"User {user_id} requested feed")  # pragma: no mutate
    dummy_msg = await msg.answer("⏳ Loading your scream...")
    await send_next_scream(user_id, dummy_msg)


@screamRouter.message(Command("top"))
async def handle_top(msg: types.Message):
    """
    Handle the /top command to display today's top screams.

    Args:
        msg (types.Message): Telegram message with /top command.

    Behavior:
        - Fetches top screams from backend
        - Sends each with content, votes and meme
        - Handles empty responses and errors
    """
    try:
        logger.info("Processing top screams request")  # pragma: no mutate
        top = await get_top_screams()
        posts = top.get("posts", [])
        if not posts:
            logger.info("No top screams available")  # pragma: no mutate
            await msg.answer("😴 No top screams today...")
            return

        logger.debug(f"Showing {len(posts)} top screams")  # pragma: no mutate
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
        logger.error(
            f"Failed to get top screams: {str(e)}",
            exc_info=True
        )  # pragma: no mutate
        await msg.answer("😴 There was an error getting top screams((")
