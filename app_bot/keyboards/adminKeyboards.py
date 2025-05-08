# Third‑party
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def deletion_keyboard_setup() -> InlineKeyboardMarkup:
    """
    Create an inline keyboard for admin scream moderation actions.

    Returns:
        InlineKeyboardMarkup:
            An inline keyboard with buttons for navigating, moderating screams.

    Buttons:
        ⬅️ - Navigate to the previous scream.
        ❌ - Delete the current scream.
        ✅ - Confirm (approve) the current scream.
        ➡️ - Navigate to the next scream.
        🚪 Exit - Exit moderation mode.
    """
    deletion_kb = InlineKeyboardBuilder()

    deletion_kb.add(
        InlineKeyboardButton(text='⬅️', callback_data='button_back'),
        InlineKeyboardButton(text='❌', callback_data='button_delete'),
        InlineKeyboardButton(text='✅', callback_data='button_confirm'),
        InlineKeyboardButton(text='➡️', callback_data='button_next'),
        InlineKeyboardButton(text='🚪 Exit', callback_data='button_exit'),
    )
    return deletion_kb.adjust(4, 1).as_markup()
