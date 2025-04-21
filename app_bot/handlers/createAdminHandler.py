from aiogram import Router, types
from aiogram.filters import Command
from app_bot.api.api import create_admin  
import httpx


createAdminRouter = Router()

@createAdminRouter.message(Command("create_admin"))
async def handle_create_admin(msg: types.Message):
    args = msg.text.split()

    if len(args) != 2:
        await msg.answer("Usage: /create_admin <user_id>")
        return

    user_id_to_admin = args[1]
    user_id = str(msg.from_user.id) 

    try:
        result = await create_admin(user_id, user_id_to_admin)

        if result.get("status") == "ok":
            await msg.answer(f"User {user_id_to_admin} is now an admin!")
        elif result.get("status") == "already_admin":
            await msg.answer("This user is already an admin.")
        else:
            await msg.answer("Something went wrong.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            await msg.answer("You do not have permission — only admins can perform this action.")
        else:
            await msg.answer("Server error occurred.")
    except Exception as e:
        await msg.answer("Failed to assign admin rights.")