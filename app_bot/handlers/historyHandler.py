# Standard library
import logging

# Third‑party
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

# Local application
from app_bot.api.api import get_history, get_historical_week
from app_bot.keyboards.adminKeyboards import history_keyboard


logger = logging.getLogger("app_bot")

historyRouter = Router()

@historyRouter.message(Command("history"))
async def handle_history(msg: types.Message):
    """
    Handle the /history command to display available archived weeks.

    Args:
        msg (types.Message): Telegram message from the user invoking the command.

    Behavior:
        - Fetches a list of archived weeks from the backend.
        - If archives exist, sends a message with an inline keyboard for week selection.
        - If no archives exist, notifies the user that the archive is empty.
        - On error, logs the issue and informs the user.
    """
    try:
        weeks = await get_history()
        if not weeks:
            await msg.answer("Archive is empty")
            return
            
        await msg.answer(
            "📆 Choose a week:",
            reply_markup=history_keyboard(weeks)
        )
    except Exception as e:
        logger.error(f"History error: {str(e)}", exc_info=True)
        await msg.answer("❌ Error loading history")

@historyRouter.callback_query(F.data.startswith("week_"))
async def handle_week_selection(callback: CallbackQuery):
    """
    Handle a callback query for selecting a specific archived week.

    Args:
        callback (CallbackQuery): Telegram callback query triggered by week selection.

    Behavior:
        - Extracts the week ID from the callback data.
        - Retrieves the top screams for that week.
        - Formats and sends a message with the top 3 screams, including votes and meme links.
        - If no data is found for the selected week, informs the user.
        - Logs any errors and sends a generic failure message if needed.
    """
    try:
        week_id = callback.data.split("_")[1]
        await callback.answer("⏳ Loading weekly top...")
        
        week_data = await get_historical_week(week_id)
        top_screams = week_data.get("posts", [])[:3]

        if not top_screams:
            await callback.message.answer(f"🚫 No data for the week {week_id}")
            return

        response = [
            f"🏆 Week {week_id} top:",
            *[
                f"{i}. {scream['content']}\n"
                f"❤️ Reactions: {scream['votes']}\n"
                f"🔗 Meme: {scream['meme_url'] if scream['meme_url'] else 'нет'}"
                for i, scream in enumerate(top_screams, 1)
            ]
        ]
        
        await callback.message.edit_text(
            text="\n\n".join(response),
            reply_markup=None
        )

    except Exception as e:
        logger.error(f"Week selection error: {str(e)}", exc_info=True)
        await callback.message.answer("❌ Error loading week data")
        await callback.answer()