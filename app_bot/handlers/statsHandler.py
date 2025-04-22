from aiogram import Router, types
from app_bot.api.api import get_stress_stats, get_user_stats
from aiogram.filters import Command


statsRouter = Router()

@statsRouter.message(Command("stress"))
async def handle_stress(msg: types.Message):
    stats = await get_stress_stats()
    temp = stats.get('chart_url')
    await msg.answer(f"<b>📊 This week stress level</b>\n{temp}", parse_mode="HTML")
    


@statsRouter.message(Command("my_stats"))
async def handle_user_stats(msg: types.Message):
    user_id = str(msg.from_user.id)

    stats = await get_user_stats(user_id)
    await msg.answer(
        "<b>📊 Your Scream Stats</b>\n\n"
        f"🗯️ <b>Screams posted:</b> {stats.get('screams_posted')}\n"
        f"💥 <b>Reactions given:</b> {stats.get('reactions_given')}\n"
        f"❤️ <b>Reactions received:</b> {stats.get('reactions_got')}",
        parse_mode="HTML"
    )
    temp = stats.get('chart_url')
    await msg.answer(
        "📊 <b>Your personal stress chart</b>\n"
        "This chart visualizes your recent scream activity and reactions:\n"
        f"{temp}",
        parse_mode="HTML"
    )