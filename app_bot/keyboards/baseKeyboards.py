# Third‑party
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def reaction_keyboard(scream_id: int):
    """
    Generate an inline keyboard for reacting to a scream.

    Args:
        scream_id (int): The ID of the scream to associate with the reaction buttons.

    Returns:
        InlineKeyboardMarkup: An inline keyboard with:
            - Three emoji reaction buttons,
            - A "Skip" button to skip the scream,
            - An "Exit" button to leave the feed.
    """
    emojis = ["💀", "🔥", "🤡"]
    buttons = [
        InlineKeyboardButton(text=emoji, callback_data=f"react:{scream_id}:{emoji}")
        for emoji in emojis
    ]
    exit_button = InlineKeyboardButton(text="🚪 Exit", callback_data="exit_feed")
    skip_button = InlineKeyboardButton(text="❌ Skip", callback_data=f"react:{scream_id}:❌")
    return InlineKeyboardMarkup(inline_keyboard=[buttons, [skip_button], [exit_button]])
