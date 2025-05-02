# Third‑party
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def deletion_keyboard_setup() -> InlineKeyboardMarkup:
    """
    Create an inline keyboard for admin scream moderation actions.

    Returns:
        InlineKeyboardMarkup: An inline keyboard with buttons for navigating and moderating screams.

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


def history_keyboard(weeks: list) -> InlineKeyboardMarkup:
    """
    Create an inline keyboard for selecting archived weeks.

    Args:
        weeks (list): A list of week identifiers in the format 'YYYY-WW'.

    Returns:
        InlineKeyboardMarkup: An inline keyboard with buttons for each available archive week.

    Buttons:
        🗓 WW-YYYY — where WW is the week number and YYYY is the year.
    """
    builder = InlineKeyboardBuilder()
    for week in weeks:
        year, week_num = week.split('-')
        builder.add(InlineKeyboardButton(
            text=f"🗓 {week_num}-{year}",
            callback_data=f"week_{week}"
        ))
    builder.adjust(2)
    return builder.as_markup()