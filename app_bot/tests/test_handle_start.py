import pytest
from unittest.mock import AsyncMock, MagicMock

from app_bot.handlers.startHandler import handle_start


@pytest.mark.asyncio
async def test_handle_start():
    """
    Test the /start command handler.

    - Simulates a /start message from a user.
    - Verifies that the welcome message is sent.
    - Verifies that user ID is logged and parsed correctly.
    """
    msg = MagicMock()
    msg.from_user.id = 12345
    msg.answer = AsyncMock()

    await handle_start(msg)

    msg.answer.assert_awaited_with(
        "🗯️ <b>Welcome to InnoScreamBot</b>\n\n"
        "An anonymous place to let it all out. Here's what you can do:\n\n"
        "<b>😤 /scream [text]</b> — Post your scream anonymously\n"
        "<b>🔥 React to screams</b> — Vote with emojis\n"
        "<b>📊 /stats</b> — See your scream & reactions count\n"
        "<b>📈 /stress</b> — View weekly stress graphs\n"
        "<b>📚 /history</b> — Browse top screams from past weeks\n"
        "<b>🏆 /top</b> — View the top scream of the day (with memes!)\n\n"
        "Let's scream it out. You in?",
        parse_mode="HTML"
    )
