# Third‑party
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


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
