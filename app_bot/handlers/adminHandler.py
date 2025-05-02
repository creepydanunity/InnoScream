import httpx
from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from app_bot.FSM.admin import AdminScreamReview
from app_bot.api.api import confirm_scream, delete_scream, get_all_screams_for_admin
from app_bot.keyboards.adminKeyboards import deletion_keyboard_setup
from aiogram.types import CallbackQuery
from app_bot.api.api import create_admin, delete_scream
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app_bot.logger import logger

adminRouter = Router()

@adminRouter.message(Command("delete"))
async def handle_delete(msg: types.Message, state: FSMContext):
    """
    Handle the /delete command to start a moderation session.

    Args:
        msg (types.Message): Telegram message containing the delete command.
        state (FSMContext): Finite State Machine context for tracking the moderation session.

    Behavior:
        - Retrieves unmoderated screams from the API.
        - Displays the first scream to the admin for review.
        - Sets the FSM state to reviewing.
    """

    screams = []
    try:
        screams = await get_all_screams_for_admin(str(msg.from_user.id))
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            await msg.answer("🎉 All screams are already reviewed.")
        elif e.response.status_code == 403:
            await msg.answer("You do not have permission — only admins can perform this action.")
        return

    try:
        user_id = str(msg.from_user.id)
        
        if not screams:
            logger.info("No screams available for moderation")
            await msg.answer("😴 No screams available.")
            return
        
        logger.info(f"Admin {user_id} started moderation session")

        scream_index = 0
        await state.update_data(screams=screams, index=scream_index)
        await state.set_state(AdminScreamReview.reviewing)

        current = screams[scream_index]
        logger.debug(f"Displaying scream {current['scream_id']} to admin")

        await msg.answer(
            text=f"🧠 Scream {scream_index + 1} out of {len(screams)}:\n\n📌Scream_id: {current['scream_id']}\n\n📝Content:\n{current['content']}",
            reply_markup=deletion_keyboard_setup()
        )
    except Exception as e:
        logger.error(f"Failed to start moderation: {str(e)}", exc_info=True)
        await msg.answer("❌ Failed to start moderation")

@adminRouter.callback_query(F.data.startswith('button_back'))
async def process_callback_button_back(callback_query: CallbackQuery, state: FSMContext):
    """
    Handle the "button back" action in the scream moderation feed.

    Args:
        callback_query (CallbackQuery): Telegram callback query signaling a back navigation.
        state (FSMContext): FSM context containing moderation state and scream list.

    Behavior:
        - Navigates to the previous scream.
        - Updates the message with the previous scream's content and options.
    """

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

@adminRouter.message(Command("create_admin"))
async def handle_create_admin(msg: types.Message):
    """
    Handle the /create_admin command to assign admin rights.

    Args:
        msg (types.Message): Telegram message containing the command and user ID.

    Behavior:
        - Validates the input format.
        - Calls the API to create a new admin.
        - Sends a success or error message based on the result.
    """

    try:
        args = msg.text.split()
        user_id = str(msg.from_user.id)
        
        if len(args) != 2:
            logger.warning(f"Invalid create_admin command format from user {user_id}")
            await msg.answer("Usage: /create_admin <user_id>")
            return

        user_id_to_admin = args[1]
        logger.info(f"Admin creation attempt by {user_id} for {user_id_to_admin}")

        result = await create_admin(user_id, user_id_to_admin)

        if result.get("status") == "ok":
            logger.info(f"Successfully created admin {user_id_to_admin}")
            await msg.answer(f"User {user_id_to_admin} is now an admin!")
        elif result.get("status") == "already_admin":
            logger.info(f"User {user_id_to_admin} is already admin")
            await msg.answer("This user is already an admin.")
        else:
            logger.warning(f"Unknown response when creating admin: {result}")
            await msg.answer("Something went wrong.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            logger.warning(f"Permission denied for user {user_id}")
            await msg.answer("You do not have permission — only admins can perform this action.")
        else:
            logger.error(f"HTTP error in create_admin: {str(e)}", exc_info=True)
            await msg.answer("Server error occurred.")
    except Exception as e:
        logger.error(f"Failed to assign admin rights: {str(e)}", exc_info=True)
        await msg.answer("Failed to assign admin rights.")

@adminRouter.callback_query(F.data.startswith('button_delete'))
async def process_callback_button_delete(callback_query: CallbackQuery, state: FSMContext):
    """
    Handle the "delete button" action for a scream in the moderation feed.

    Args:
        callback_query (CallbackQuery): Telegram callback query signaling a delete action.
        state (FSMContext): FSM context containing moderation state and scream list.

    Behavior:
        - Sends a request to delete the current scream.
        - Displays the next scream or ends the session if none are left.
    """

    try:
        data = await state.get_data()
        screams = data["screams"]
        index = data["index"]
        current = screams[index]
        user_id = str(callback_query.from_user.id)
        
        logger.info(f"Admin {user_id} deleting scream {current['scream_id']}")

        result = await delete_scream(current['scream_id'], user_id)

        if result['status'] == "deleted":
            logger.info(f"Scream {current['scream_id']} deleted successfully")
            await callback_query.message.edit_text(
                text=f"🗑️ Deleted scream:\n\n{current['content']}",
                reply_markup=None
            )

            screams.pop(index)
            if not screams:
                logger.info("All screams reviewed")
                await state.clear()
                await callback_query.message.answer("✅ All screams reviewed.")
                return

            index = index % len(screams)
            await state.update_data(screams=screams, index=index)

            next_scream = screams[index]
            logger.debug(f"Showing next scream {next_scream['scream_id']}")

            await callback_query.message.answer(
                text=f"🧠 Scream {index + 1} out of {len(screams)}:\n\n📌Scream_id: {next_scream['scream_id']}\n\n📝Content:\n{next_scream['content']}",
                reply_markup=deletion_keyboard_setup()
            )
        else:
            logger.warning(f"Failed to delete scream {current['scream_id']}")
            await callback_query.message.answer("🤔 Couldn't delete scream.")
    except Exception as e:
        logger.error(f"Failed to process delete action: {str(e)}", exc_info=True)
        await callback_query.answer("❌ Deletion failed")

@adminRouter.callback_query(F.data.startswith('button_confirm'))
async def process_callback_button_confirm(callback_query: CallbackQuery, state: FSMContext):
    """
    Handle the "button confirm" action for a scream in the moderation feed.

    Args:
        callback_query (CallbackQuery): Telegram callback query signaling a confirm action.
        state (FSMContext): FSM context containing moderation state and scream list.

    Behavior:
        - Sends a request to confirm the current scream.
        - Displays the next scream or ends the session if none are left.
    """

    try:
        data = await state.get_data()
        screams = data["screams"]
        index = data["index"]
        current = screams[index]
        user_id = str(callback_query.from_user.id)
        
        logger.info(f"Admin {user_id} confirming scream {current['scream_id']}")

        result = await confirm_scream(current['scream_id'], user_id)

        if result['status'] == "confirmed":
            logger.info(f"Scream {current['scream_id']} confirmed")
            await callback_query.message.edit_text(
                text=f"✅ Confirmed scream:\n\n{current['content']}",
                reply_markup=None
            )

            screams.pop(index)
            if not screams:
                logger.info("All screams reviewed")
                await state.clear()
                await callback_query.message.answer("🎉 All screams reviewed.")
                return

            index = index % len(screams)
            await state.update_data(screams=screams, index=index)

            next_scream = screams[index]
            logger.debug(f"Showing next scream {next_scream['scream_id']}")

            await callback_query.message.answer(
                text=f"🧠 Scream {index + 1} out of {len(screams)}:\n\n📌Scream_id: {next_scream['scream_id']}\n\n📝Content:\n{next_scream['content']}",
                reply_markup=deletion_keyboard_setup()
            )
        else:
            logger.warning(f"Failed to confirm scream {current['scream_id']}")
            await callback_query.message.answer("🤔 Could not confirm scream.")
    except Exception as e:
        logger.error(f"Failed to process confirmation: {str(e)}", exc_info=True)
        await callback_query.answer("❌ Confirmation failed")

@adminRouter.callback_query(F.data.startswith('button_next'))
async def process_callback_button_next(callback_query: CallbackQuery, state: FSMContext):
    """
    Handle the 'button next" action in the scream moderation feed.

    Args:
        callback_query (CallbackQuery): Telegram callback query signaling a next action.
        state (FSMContext): FSM context containing moderation state and scream list.

    Behavior:
        - Moves to the next scream in the list.
        - Updates the message with the next scream's content and options.
    """

    try:
        data = await state.get_data()
        scream_index = (data["index"] + 1) % len(data["screams"])
        screams = data["screams"]
        current = screams[scream_index]
        
        logger.debug(f"Admin navigating to next scream {current['scream_id']}")

        await state.update_data(screams=screams, index=scream_index)
        
        await callback_query.message.edit_text(
            text=f"🧠 Scream {scream_index + 1} out of {len(screams)}:\n\n📌Scream_id: {current['scream_id']}\n\n📝Content:\n{current['content']}",
            reply_markup=deletion_keyboard_setup()
        )
    except Exception as e:
        logger.error(f"Failed to navigate next: {str(e)}", exc_info=True)
        await callback_query.answer("❌ Navigation error")

@adminRouter.callback_query(F.data == 'button_exit')
async def process_callback_button_exit(callback_query: CallbackQuery, state: FSMContext):
    """
    Handle the "exit button" action from the scream feed.

    Args:
        callback_query (CallbackQuery): Telegram callback query signaling the exit action.
        state (FSMContext): FSM context to be cleared.

    Behavior:
        - Clears the moderation session state.
        - Edits the current message to display an exit confirmation.
    """

    try:
        user_id = str(callback_query.from_user.id)
        logger.info(f"Admin {user_id} exited moderation mode")
        await state.clear()
        await callback_query.message.edit_text("🚪 Exited moderation mode.", reply_markup=None)
    except Exception as e:
        logger.error(f"Failed to exit moderation: {str(e)}", exc_info=True)
        await callback_query.answer("❌ Exit failed")