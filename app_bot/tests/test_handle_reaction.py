import pytest
from unittest.mock import AsyncMock, MagicMock
from app_bot.handlers.reactionHandler import handle_reaction


@pytest.mark.asyncio
async def test_handle_reaction_success(monkeypatch):
    """Test successful reaction and loading of next scream."""
    callback = MagicMock()
    callback.data = "react:123:🔥"
    callback.from_user.id = 99
    callback.answer = AsyncMock()
    callback.message = MagicMock()

    monkeypatch.setattr(
        "app_bot.handlers.reactionHandler.react_to_scream",
        AsyncMock()
    )
    monkeypatch.setattr(
        "app_bot.handlers.reactionHandler.send_next_scream",
        AsyncMock()
    )

    await handle_reaction(callback)
    callback.answer.assert_awaited_with("🔥 accepted!")
    from app_bot.handlers.reactionHandler import send_next_scream
    send_next_scream.assert_awaited_once_with("99", callback.message)


@pytest.mark.asyncio
async def test_handle_reaction_fail(monkeypatch):
    """Test reaction failure sends failure message."""
    callback = MagicMock()
    callback.data = "react:123:❌"
    callback.from_user.id = 88
    callback.answer = AsyncMock()
    callback.message = MagicMock()

    async def fail(*args, **kwargs):
        raise RuntimeError("Already reacted")

    monkeypatch.setattr(
        "app_bot.handlers.reactionHandler.react_to_scream",
        fail
    )

    await handle_reaction(callback)
    callback.answer.assert_awaited_with("❌ Already reacted!")
