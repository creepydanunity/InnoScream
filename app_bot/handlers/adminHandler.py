from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from app_bot.FSM.admin import AdminScreamReview
from app_bot.api.api import confirm_scream, delete_scream, get_all_screams_for_admin
from app_bot.keyboards.adminKeyboards import deletion_keyboard_setup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


adminRouter = Router()

@adminRouter.message(Command("delete"))
async def handle_delete(msg: types.Message, state: FSMContext):
    screams = await get_all_screams_for_admin(str(msg.from_user.id))

    if not screams:
        await msg.answer("😴 No screams available.")
        return

    scream_index = 0

    await state.update_data(screams=screams, index=scream_index)
    await state.set_state(AdminScreamReview.reviewing)

    current = screams[scream_index]

    await msg.answer(
        text=f"🧠 Scream {scream_index + 1} out of {len(screams)}:\n\n📌Scream_id: {current['scream_id']}\n\n📝Content:\n{current['content']}",
        reply_markup=deletion_keyboard_setup()
    )

@adminRouter.callback_query(F.data.startswith('button_back'))
async def process_callback_button_back(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    scream_index = (data["index"] - 1) % len(data["screams"])
    screams = data["screams"]

    data["index"] = scream_index
    current = screams[scream_index]

    await state.update_data(screams=screams, index=scream_index)

    await callback_query.message.edit_text(
        text=f"🧠 Scream {scream_index + 1} out of {len(screams)}:\n\n📌Scream_id: {current['scream_id']}\n\n📝Content:\n{current['content']}",
        reply_markup=deletion_keyboard_setup()
    )

@adminRouter.callback_query(F.data.startswith('button_delete'))
async def process_callback_button_delete(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    screams = data["screams"]
    index = data["index"]
    current = screams[index]

    result = await delete_scream(current['scream_id'], str(callback_query.from_user.id))

    if result['status'] == "deleted":
        await callback_query.message.edit_text(
            text=f"🗑️ Deleted scream:\n\n{current['content']}",
            reply_markup=None
        )

        screams.pop(index)
        if not screams:
            await state.clear()
            await callback_query.message.answer("✅ All screams reviewed.")
            return

        index = index % len(screams)
        await state.update_data(screams=screams, index=index)

        next_scream = screams[index]
        await callback_query.message.answer(
            text=f"🧠 Scream {index + 1} out of {len(screams)}:\n\n📌Scream_id: {next_scream['scream_id']}\n\n📝Content:\n{next_scream['content']}",
            reply_markup=deletion_keyboard_setup()
        )
    else:
        await callback_query.message.answer("🤔 Couldn't delete scream.")

@adminRouter.callback_query(F.data.startswith('button_confirm'))
async def process_callback_button_confirm(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    screams = data["screams"]
    index = data["index"]
    current = screams[index]

    result = await confirm_scream(current['scream_id'], str(callback_query.from_user.id))

    if result['status'] == "confirmed":
        await callback_query.message.edit_text(
            text=f"✅ Confirmed scream:\n\n{current['content']}",
            reply_markup=None
        )

        screams.pop(index)
        if not screams:
            await state.clear()
            await callback_query.message.answer("🎉 All screams reviewed.")
            return

        index = index % len(screams)
        await state.update_data(screams=screams, index=index)

        next_scream = screams[index]
        await callback_query.message.answer(
            text=f"🧠 Scream {index + 1} out of {len(screams)}:\n\n📌Scream_id: {next_scream['scream_id']}\n\n📝Content:\n{next_scream['content']}",
            reply_markup=deletion_keyboard_setup()
        )
    else:
        await callback_query.message.answer("🤔 Could not confirm scream.")

@adminRouter.callback_query(F.data.startswith('button_next'))
async def process_callback_button_next(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    scream_index = (data["index"] + 1) % len(data["screams"])
    screams = data["screams"]

    data["index"] = scream_index
    current = screams[scream_index]

    await state.update_data(screams=screams, index=scream_index)
    
    await callback_query.message.edit_text(
        text=f"🧠 Scream {scream_index + 1} out of {len(screams)}:\n\n📌Scream_id: {current['scream_id']}\n\n📝Content:\n{current['content']}",
        reply_markup=deletion_keyboard_setup()
    )

@adminRouter.callback_query(F.data == 'button_exit')
async def process_callback_button_exit(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text("🚪 Exited moderation mode.", reply_markup=None)