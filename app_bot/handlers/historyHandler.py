from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from app_bot.api.api import get_history, get_historical_week
from app_bot.keyboards.adminKeyboards import history_keyboard
import logging

logger = logging.getLogger("app_bot")

historyRouter = Router()

@historyRouter.message(Command("history"))
async def handle_history(msg: types.Message):
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
    try:
        week_id = callback.data.split("_")[1]
        await callback.answer("⏳ Loading weekly top...")
        
        week_data = await get_historical_week(week_id)
        top_screams = week_data.get("posts", [])[:3]

        if not top_screams:
            await callback.message.answer(f"🚫 No data for the week {week_id}")
            return

        response = [
            f"🏆 Топ-3 за неделю {week_id}:",
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