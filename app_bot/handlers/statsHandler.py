from aiogram import Router, types
from app_bot.api.api import get_stress_stats, get_user_stats
from aiogram.filters import Command


statsRouter = Router()


@statsRouter.message(Command("stress"))
async def handle_stress(msg: types.Message):
    """
    Handle the /stress command to display a collective stress chart.

    Args:
        msg (types.Message): Incoming Telegram message containing the /stress command.

    Behavior:
        - Fetches the weekly scream statistics from the backend.
        - Sends a bar chart image showing the number of screams per day over the past week.
    """

    stats = await get_stress_stats()
    await msg.answer_photo(
        photo=stats.get("chart_url"),
        caption="📉 <b>This week's collective stress level</b>",
        parse_mode="HTML"
    )


@statsRouter.message(Command("stats"))
async def handle_user_stats(msg: types.Message):
    """
    Handle the /stats command to display a user's scream activity statistics.

    Args:
        msg (types.Message): Incoming Telegram message containing the /stats command.

    Behavior:
        - Retrieves the user's statistics from the backend API.
        - Sends a message summarizing the user's total screams, reactions given, and reactions received.
        - Sends two charts:
            - A bar chart showing daily scream activity over the past week.
            - A pie chart showing the distribution of reactions received.
    """

    user_id = str(msg.from_user.id)
    stats = await get_user_stats(user_id)

    caption = (
        "<b>📊 Your scream stats</b>\n\n"
        f"😤 <b>Screams posted:</b> {stats.get('screams_posted')}\n"
        f"💬 <b>Reactions given:</b> {stats.get('reactions_given')}\n"
        f"🔥 <b>Reactions received:</b> {stats.get('reactions_got')}\n"
    )

    await msg.answer(caption, parse_mode="HTML")

    await msg.answer_photo(
        photo=stats.get("chart_url"),
        caption="📈 <b>Your personal stress chart</b>",
        parse_mode="HTML"
    )

    await msg.answer_photo(
    photo=stats.get("reaction_chart_url"),
    caption="🎭 <b>Reactions your screams received</b>",
    parse_mode="HTML"
)