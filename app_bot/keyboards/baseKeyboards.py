from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def reaction_keyboard(scream_id: int):
    emojis = ["💀", "🔥", "🤡"]
    buttons = [
        InlineKeyboardButton(text=emoji, callback_data=f"react:{scream_id}:{emoji}")
        for emoji in emojis
    ]
    exit_button = InlineKeyboardButton(text="🚪 Exit", callback_data="exit_feed")
    skip_button = InlineKeyboardButton(text="❌ Skip", callback_data=f"react:{scream_id}:❌")
    return InlineKeyboardMarkup(inline_keyboard=[buttons, [skip_button], [exit_button]])
