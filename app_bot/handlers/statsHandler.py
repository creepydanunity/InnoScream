from aiogram import Router, types
from app_bot.api.api import get_stress_stats, get_user_stats


statsRouter = Router()

@statsRouter.message(commands=["stress"])
async def handle_stress(msg: types.Message):
    stats = await get_stress_stats()
    await msg.answer(f"This week stress level:\n\n{stats.get("chart_url")}")
    


@statsRouter.message(commands=["my_stats"])
async def handle_user_stats(msg: types.Message):
    user_id = str(msg.from_user.id)

    stats = await get_user_stats(user_id)
    await msg.answer(f"Screams posted: {stats.get("screams_posted")}\n" + 
                     f"Reactions given: {stats.get("reactions_given")}\n" +
                     f"Reactions got: {stats.get("reactions_got")}\n")
    
    await msg.answer(f"Your personal stress chart:\n\n{stats.get("chart_url")}")