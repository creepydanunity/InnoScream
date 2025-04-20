from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def reaction_keyboard(scream_id: int):
    emojis = ["💀", "🔥", "🤡", "❌"]
    buttons = [
        InlineKeyboardButton(text=emoji, callback_data=f"react:{scream_id}:{emoji}")
        for emoji in emojis
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
