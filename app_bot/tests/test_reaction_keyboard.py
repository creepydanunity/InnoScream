from app_bot.keyboards.baseKeyboards import reaction_keyboard
from aiogram.types import InlineKeyboardMarkup


def test_reaction_keyboard_structure():
    """Test that reaction_keyboard returns the correct button layout and callback data."""
    scream_id = 123
    keyboard = reaction_keyboard(scream_id)

    assert isinstance(keyboard, InlineKeyboardMarkup)

    rows = keyboard.inline_keyboard
    assert len(rows[0]) == 3
    assert [btn.text for btn in rows[0]] == ["💀", "🔥", "🤡"]
    assert all(btn.callback_data.startswith(f"react:{scream_id}:") for btn in rows[0])
    skip = rows[1][0]
    assert skip.text == "❌ Skip"
    assert skip.callback_data == f"react:{scream_id}:❌"
    exit_btn = rows[2][0]
    assert exit_btn.text == "🚪 Exit"
    assert exit_btn.callback_data == "exit_feed"
