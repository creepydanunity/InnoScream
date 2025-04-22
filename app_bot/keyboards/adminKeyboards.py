from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def deletion_keyboard_setup() -> InlineKeyboardMarkup:
    deletion_kb = InlineKeyboardBuilder()

    deletion_kb.add(
        InlineKeyboardButton(text='⬅️', callback_data='button_back'),
        InlineKeyboardButton(text='❌', callback_data='button_delete'),
        InlineKeyboardButton(text='✅', callback_data='button_confirm'),
        InlineKeyboardButton(text='➡️', callback_data='button_next'),
        InlineKeyboardButton(text='🚪 Exit', callback_data='button_exit'),
    )
    

    return deletion_kb.adjust(4, 1).as_markup()