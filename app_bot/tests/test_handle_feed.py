import pytest
from unittest.mock import AsyncMock, MagicMock

from app_bot.handlers.screamHandler import handle_feed
from app_bot.handlers.reactionHandler import handle_exit_feed


@pytest.mark.asyncio
async def test_handle_feed(monkeypatch):
    """
    Test that /feed command triggers a loading message, sends the next scream.
    """
    msg = MagicMock()
    msg.answer = AsyncMock(return_value=MagicMock())
    msg.from_user.id = 42

    dummy_msg = await msg.answer("⏳ Loading your scream...")

    monkeypatch.setattr(
        "app_bot.handlers.screamHandler.send_next_scream",
        AsyncMock()
    )
    await handle_feed(msg)
    msg.answer.assert_awaited_with("⏳ Loading your scream...")
    from app_bot.handlers.screamHandler import send_next_scream
    send_next_scream.assert_awaited_once_with("42", dummy_msg)


@pytest.mark.asyncio
async def test_handle_exit_feed():
    """
    Test that the exit_feed callback edits the message and sends confirmation.
    """
    callback = MagicMock()
    callback.from_user.id = 123
    callback.answer = AsyncMock()

    msg = MagicMock()
    msg.edit_text = AsyncMock()
    callback.message = msg

    await handle_exit_feed(callback)

    msg.edit_text.assert_awaited_with(
        "👋 <i>You've exited the scream feed</i>",
        parse_mode="HTML"
    )
    callback.answer.assert_awaited()
