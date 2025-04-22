from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from app_bot.api.api import get_next_scream, delete_scream, get_all_screams_for_admin
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

scream_index = 0
screams = []

@adminRouter.message(Command("delete"))
async def handle_delete(msg: types.Message):
    global scream_index, screams

    screams = await get_all_screams_for_admin()
    if not screams:
        await msg.answer("😴 No screams available.")
        return

    scream_index = 0
    current = screams[scream_index]

    await msg.answer(
        text=f"🧠 Scream {scream_index + 1} out of {len(screams)}:\n\n📌Scream_id: {current['scream_id']}\n\n📝Content:\n{current['content']}",
        reply_markup=inline_kb
    )

@adminRouter.callback_query(F.data == 'button_back')
async def process_callback_button_back(callback_query: CallbackQuery):
    global scream_index, screams

    scream_index -= 1

    if not screams:
        await callback_query.message.answer("😴 No screams available.")
        return
    
    if scream_index < 0:
        scream_index = len(screams) - 1

    current = screams[scream_index]
    await callback_query.message.edit_text(
        text=f"🧠 Scream {scream_index + 1} out of {len(screams)}:\n\n📌Scream_id: {current['scream_id']}\n\n📝Content:\n{current['content']}",
        reply_markup=inline_kb
    )

@adminRouter.callback_query(F.data == 'button_delete')
async def process_callback_button_delete(callback_query: CallbackQuery):
    global scream_index, screams

    current = screams[scream_index]

    result = await delete_scream(current['scream_id'], str(callback_query.from_user.id))

    if result['status'] == "deleted":
        deleted_text = f"🗑️ Scream {scream_index + 1} deleted:\n\n{current['content']}"

        screams.pop(scream_index)
        if scream_index >= len(screams):
            scream_index = 0

        await callback_query.message.edit_text(deleted_text, reply_markup=None)

        if screams:
            next_scream = screams[scream_index]

            await callback_query.message.answer(
                text=f"🧠 Scream {scream_index + 1} out of {len(screams)}:\n\n📌Scream_id: {next_scream['scream_id']}\n\n📝Content:\n{next_scream['content']}",
                reply_markup=inline_kb
            )
        else:
            await callback_query.message.answer("✅ All screams reviewed. Nothing left!", reply_markup=None)

    else:
        await callback_query.message.answer(f"🤔 Couldn't delete scream.")

@adminRouter.callback_query(F.data == 'button_confirm')
async def process_callback_button_confirm(callback_query: CallbackQuery):
    # TODO: добавить логику для confirm of scream from admin
    await callback_query.message.edit_text('Это сделает Ваниль Дасильев!', reply_markup=inline_kb)

@adminRouter.callback_query(F.data == 'button_next')
async def process_callback_button_next(callback_query: CallbackQuery):
    global scream_index, screams
    scream_index += 1
    
    if not screams:
        await callback_query.message.answer("😴 No screams available.")
        return
    
    if scream_index >= len(screams):
        scream_index = 0

    current = screams[scream_index]
    await callback_query.message.edit_text(
        text=f"🧠 Scream {scream_index + 1} out of {len(screams)}:\n\n📌Scream_id: {current['scream_id']}\n\n📝Content:\n{current['content']}",
        reply_markup=inline_kb
    )