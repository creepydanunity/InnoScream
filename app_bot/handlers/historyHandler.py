# Standard library
import logging

# Third-party
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

# Local application
from app_bot.api.api import get_history, get_historical_week
from app_bot.keyboards.historyKeyboards import history_keyboard


logger = logging.getLogger("app_bot")

historyRouter = Router()


@historyRouter.message(Command("history"))
async def handle_history(msg: types.Message):
    """
    Handle the /history command to display available archived weeks.

    Args:
        msg (types.Message): Telegram message from user.

    Behavior:
        - Fetches archived weeks from backend
        - Shows inline keyboard for selection if exists
        - Handles empty archive and errors
    """
    try:
        weeks = await get_history()
        if not weeks:
            await msg.answer(
                "❌ There is no archived top yet"
            )
            return
        await msg.answer(
            "📆 Choose a week:",
            reply_markup=history_keyboard(weeks)
        )
    except Exception as e:
        logger.error(
            f"History error: {str(e)}",
            exc_info=True
        )
        await msg.answer("❌ Error loading history")


@historyRouter.callback_query(F.data.startswith("week_"))
async def handle_week_selection(callback: CallbackQuery):
    """
    Handle callback for selecting archived week.

    Args:
        callback (CallbackQuery): Callback with week selection.

    Behavior:
        - Gets week data
        - Shows top 3 screams with votes and memes
        - Handles empty data and errors
    """
    try:
        week_id = callback.data.split("_")[1]
        await callback.answer(
            "⏳ Loading weekly top..."
        )
        week_data = await get_historical_week(week_id)
        top_screams = week_data.get("posts", [])[:3]

        if not top_screams:
            await callback.message.answer(
                f"🚫 No data for the week {week_id}"
            )
            return

        response = [
            f"🏆 Week {week_id} top:",
            *[
                f"{i}. {scream['content']}\n"
                f"❤️ Reactions: {scream['votes']}\n"
                f"🔗 Meme: {scream['meme_url'] or 'нет'}"
                for i, scream in enumerate(top_screams, 1)
            ]
        ]
        await callback.message.edit_text(
            text="\n\n".join(response),
            reply_markup=None
        )

    except Exception as e:
        logger.error(
            f"Week selection error: {str(e)}",
            exc_info=True
        )
        await callback.message.answer(
            "❌ Error loading week data"
        )
        await callback.answer()
