import pytest
from unittest.mock import AsyncMock, MagicMock

from app_bot.handlers.statsHandler import handle_user_stats


@pytest.mark.asyncio
async def test_handle_user_stats_success(monkeypatch, caplog):
    """
    Test successful /stats command.

    - Mocks API call to return sample stats and chart URLs.
    - Asserts bot sends summary + 2 chart images.
    - Verifies logging.
    """
    msg = MagicMock()
    msg.answer = AsyncMock()
    msg.answer_photo = AsyncMock()
    msg.from_user.id = 123

    mock_stats = {
        "screams_posted": 4,
        "reactions_given": 10,
        "reactions_got": 6,
        "chart_url": "http://image/chart.png",
        "reaction_chart_url": "http://image/reactions.png"
    }

    monkeypatch.setattr(
        "app_bot.handlers.statsHandler.get_user_stats",
        AsyncMock(return_value=mock_stats)
    )

    with caplog.at_level("INFO"):
        await handle_user_stats(msg)

    assert "User 123 requested stats" in caplog.text
    msg.answer.assert_any_await(
        "<b>📊 Your scream stats</b>\n\n"
        "😤 <b>Screams posted:</b> 4\n"
        "💬 <b>Reactions given:</b> 10\n"
        "🔥 <b>Reactions received:</b> 6\n",
        parse_mode="HTML"
    )

    msg.answer_photo.assert_any_await(
        photo="http://image/chart.png",
        caption="📈 <b>Your personal stress chart</b>",
        parse_mode="HTML"
    )
    msg.answer_photo.assert_any_await(
        photo="http://image/reactions.png",
        caption="🎭 <b>Reactions your screams received</b>",
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_handle_user_stats_failure(monkeypatch, caplog):
    """Test that /stats failure is logged and error message sent."""
    msg = MagicMock()
    msg.answer = AsyncMock()
    msg.from_user.id = 456

    async def fail(*args, **kwargs):
        raise RuntimeError("backend down")

    monkeypatch.setattr(
        "app_bot.handlers.statsHandler.get_user_stats",
        fail
    )

    with caplog.at_level("ERROR"):
        await handle_user_stats(msg)
    msg.answer.assert_awaited_with("❌ Failed to load your stats")
    assert "Failed to get user stats: backend down" in caplog.text
