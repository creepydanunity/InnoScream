from aiogram import Router, types
from aiogram.filters import Command
from app_bot.api.api import get_my_id  

idRouter = Router()

@idRouter.message(Command("my_id"))
async def handle_my_id(msg: types.Message):
    user_id = str(msg.from_user.id) 

    try:
        result = await get_my_id(user_id=user_id)
        await msg.answer(f"Your user_id: {result['user_id']}")
    except Exception as e:
        await msg.answer("Failed to get user_id")

