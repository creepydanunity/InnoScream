import httpx
from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from app_bot.api.api import create_admin, get_next_scream, delete_scream
from app_bot.keyboards.baseKeyboards import reaction_keyboard
from aiogram.filters import Command


adminRouter = Router()

inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='⬅️', callback_data='button_back'),
             InlineKeyboardButton(text='❌', callback_data='button_delete'),
             InlineKeyboardButton(text='✅', callback_data='button_confirm'),
             InlineKeyboardButton(text='➡️', callback_data='button_next')]
        ]
    )

@adminRouter.message(Command("create_admin"))
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
        
@adminRouter.message(Command("delete"))
async def handle_delete(msg: types.Message):
    await msg.answer("SCREAM", reply_markup=inline_kb)

@adminRouter.callback_query(F.data == 'button_back')
async def process_callback_button_back(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Нажата button_back кнопка!', reply_markup=inline_kb)

@adminRouter.callback_query(F.data == 'button_delete')
async def process_callback_button_delete(callback_query: CallbackQuery):
    scream_id = 1
    content = "scream_text"

    result = await delete_scream(scream_id, callback_query.from_user.id)

    if result['status'] == "deleted":
        await callback_query.message.answer(f"🗑️ Scream deleted:\n\n{content}")
    else:
        await callback_query.message.answer(f"🤔 Incorrect ID recieved!")

    await callback_query.message.edit_text('Нажата button_delete кнопка!', reply_markup=inline_kb)

@adminRouter.callback_query(F.data == 'button_confirm')
async def process_callback_button_confirm(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Это сделает Ваниль Дасильев!', reply_markup=inline_kb)

@adminRouter.callback_query(F.data == 'button_next')
async def process_callback_button_next(callback_query: CallbackQuery):
    user_id = str(callback_query.from_user.id)

    await callback_query.message.edit_text('Нажата button_next кнопка!', reply_markup=inline_kb)
    
    try:
        scream = await get_next_scream(user_id)
        await callback_query.message.edit_text(
            f"🧠 New scream:\n\n{scream['content']}",
            reply_markup=inline_kb
        )
    except Exception as e:
        await callback_query.message.edit_text("😴 There is no more screams today.", reply_markup=inline_kb)