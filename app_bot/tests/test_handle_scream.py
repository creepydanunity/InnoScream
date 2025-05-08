import pytest
from unittest.mock import AsyncMock, MagicMock

from app_bot.handlers.screamHandler import handle_scream


@pytest.mark.asyncio
async def test_handle_scream_empty_content():
    """Test that the bot replies with a prompt
    when no scream content is provided."""
    msg = MagicMock()
    msg.text = "/scream"
    msg.reply = AsyncMock()
    msg.from_user.id = 123
    await handle_scream(msg)
    msg.reply.assert_awaited_with("😶 <i>What do you want to scream?</i>",
                                  parse_mode="HTML")


@pytest.mark.asyncio
async def test_handle_scream_success(monkeypatch):
    """
    Test successful scream submission using mocked post_scream().
    Verifies bot acknowledges the scream.
    """
    msg = MagicMock()
    msg.text = "/scream I’m stressed!"
    msg.answer = AsyncMock()
    msg.reply = AsyncMock()
    msg.from_user.id = 123

    fake_response = {"scream_id": "abc123"}

    monkeypatch.setattr(
        "app_bot.handlers.screamHandler.post_scream",
        AsyncMock(return_value=fake_response)
    )

    await handle_scream(msg)

    msg.answer.assert_awaited_with(
        "😤 <b>Your scream has been unleashed into the void!</b>",
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_handle_scream_failure(monkeypatch):
    """
    Test failure case where post_scream raises an exception.
    Verifies bot informs the user of the failure.
    """
    msg = MagicMock()
    msg.text = "/scream I need help"
    msg.answer = AsyncMock()
    msg.reply = AsyncMock()
    msg.from_user.id = 123

    async def boom(*args, **kwargs):
        raise RuntimeError("API offline")

    monkeypatch.setattr(
        "app_bot.handlers.screamHandler.post_scream",
        boom
    )

    await handle_scream(msg)
    msg.answer.assert_awaited_with("❌ Failed to post your scream")
