import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram import types
from app_bot.handlers.statsHandler import handle_stress


@pytest.mark.asyncio
async def test_handle_stress_success(monkeypatch):
    """
    Should send a chart image when stress stats are successfully fetched.
    """
    msg = MagicMock(spec=types.Message)
    msg.from_user = MagicMock()
    msg.from_user.id = 123
    msg.answer_photo = AsyncMock()

    monkeypatch.setattr("app_bot.handlers.statsHandler.get_stress_stats", AsyncMock(return_value={
        "chart_url": "https://example.com/chart.png"
    }))

    await handle_stress(msg)

    msg.answer_photo.assert_awaited_once_with(
        photo="https://example.com/chart.png",
        caption="📉 <b>This week's collective stress level</b>",
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_handle_stress_failure(monkeypatch):
    """
    Should send an error message when the API call fails.
    """
    msg = MagicMock(spec=types.Message)
    msg.from_user = MagicMock()
    msg.from_user.id = 456
    msg.answer = AsyncMock()

    monkeypatch.setattr("app_bot.handlers.statsHandler.get_stress_stats", AsyncMock(side_effect=Exception("API down")))

    await handle_stress(msg)

    msg.answer.assert_awaited_once_with("❌ Failed to load stress stats")
