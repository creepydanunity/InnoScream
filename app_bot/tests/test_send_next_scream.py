import pytest
from unittest.mock import AsyncMock, MagicMock

from app_bot.utils import send_next_scream


@pytest.mark.asyncio
async def test_send_next_scream_success(monkeypatch):
    """Test successful scream load and message edit with inline keyboard."""
    scream = {"scream_id": 123, "content": "This is a test scream"}

    monkeypatch.setattr(
        "app_bot.utils.get_next_scream",
        AsyncMock(return_value=scream)
    )

    fake_keyboard = MagicMock()
    monkeypatch.setattr(
        "app_bot.utils.reaction_keyboard",
        lambda scream_id: fake_keyboard
    )

    msg = MagicMock()
    msg.edit_text = AsyncMock()
    await send_next_scream("123", msg)
    msg.edit_text.assert_awaited_with(
        "😱 <b>New scream:</b>\n\n🗯️ <i>This is a test scream</i>",
        reply_markup=fake_keyboard,
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_send_next_scream_failure(monkeypatch):
    """Test fallback message when scream retrieval fails."""
    async def fail(*args, **kwargs):
        raise RuntimeError("Feed is empty")

    monkeypatch.setattr("app_bot.utils.get_next_scream", fail)

    msg = MagicMock()
    msg.edit_text = AsyncMock()
    await send_next_scream("u1", msg)
    msg.edit_text.assert_awaited_with(
        "😴 <i>No more screams in the feed for now...</i>", parse_mode="HTML"
    )
