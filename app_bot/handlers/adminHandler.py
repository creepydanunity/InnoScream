from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from app_bot.api.api import get_next_scream, delete_scream
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

@adminRouter.message(Command("delete"))
async def handle_delete(msg: types.Message):
    user_id = str(msg.from_user.id)
    content = msg.text.replace("/delete", "").strip()

    await msg.answer("SCREAM", reply_markup=inline_kb)

@adminRouter.callback_query(F.data == 'button_back')
async def process_callback_button_back(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text('Нажата button_back кнопка!', reply_markup=inline_kb)

@adminRouter.callback_query(F.data == 'button_delete')
async def process_callback_button_back(callback_query: CallbackQuery):
    await callback_query.answer()

    scream_id = 1
    content = "scream_text"

    result = await delete_scream(scream_id)

    if result['status'] == "deleted":
        await callback_query.message.answer(f"🗑️ Scream deleted:\n\n{content}")
    else:
        await callback_query.message.answer(f"🤔 Incorrect ID recieved!")

    await callback_query.message.edit_text('Нажата button_delete кнопка!', reply_markup=inline_kb)

@adminRouter.callback_query(F.data == 'button_confirm')
async def process_callback_button_back(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text('Это сделает Ваниль Дасильев!', reply_markup=inline_kb)

@adminRouter.callback_query(F.data == 'button_next')
async def process_callback_button_back(callback_query: CallbackQuery):
    await callback_query.answer()

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