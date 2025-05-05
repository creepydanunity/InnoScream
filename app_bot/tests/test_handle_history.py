import pytest
from unittest import mock
from unittest.mock import AsyncMock, patch
from aiogram import types
from aiogram.types import CallbackQuery
from app_bot.handlers.historyHandler import handle_history, handle_week_selection
from app_bot.api.api import get_history, get_historical_week

@pytest.mark.asyncio
async def test_handle_history_with_archives():
    """
    Test that handle_history sends the correct message and inline keyboard when archives are available.
    """

    mock_history = ["2023-01", "2023-02", "2023-03"]
    
    with patch("app_bot.handlers.historyHandler.get_history", return_value=mock_history):
        msg = AsyncMock(spec=types.Message)
        msg.answer = AsyncMock()
        
        await handle_history(msg)

        msg.answer.assert_called_once_with(
            "📆 Choose a week:",
            reply_markup=mock.ANY  
        )


@pytest.mark.asyncio
async def test_handle_history_no_archives():
    """
    Test that handle_history sends the correct message when no archives exist.
    """

    with patch("app_bot.handlers.historyHandler.get_history", return_value=[]):
        msg = AsyncMock(spec=types.Message)
        msg.answer = AsyncMock()
        
        await handle_history(msg)

        msg.answer.assert_called_once_with("❌ There is no archived top yet")


@pytest.mark.asyncio
async def test_handle_history_error():
    """
    Test that handle_history sends an error message when the API call fails.
    """

    with patch("app_bot.handlers.historyHandler.get_history", side_effect=Exception("API Error")):
        msg = AsyncMock(spec=types.Message)
        msg.answer = AsyncMock()
        
        await handle_history(msg)

        msg.answer.assert_called_once_with("❌ Error loading history")


@pytest.mark.asyncio
async def test_handle_week_selection_with_screams():
    """
    Test that handle_week_selection sends the correct top screams message when scream data is available for a selected week.
    """

    mock_week_data = {
        "posts": [
            {"content": "Scream 1", "votes": 5, "meme_url": "http://example.com/meme1"},
            {"content": "Scream 2", "votes": 3, "meme_url": "http://example.com/meme2"},
            {"content": "Scream 3", "votes": 4, "meme_url": "http://example.com/meme3"},
        ]
    }
    
    with patch("app_bot.handlers.historyHandler.get_historical_week", return_value=mock_week_data):
        callback = AsyncMock(spec=CallbackQuery)
        callback.data = "week_2023-01"
        callback.answer = AsyncMock()
        callback.message = AsyncMock()

        await handle_week_selection(callback)

        callback.message.edit_text.assert_called_once_with(
            text="\n\n".join([
                "🏆 Week 2023-01 top:",
                "1. Scream 1\n❤️ Reactions: 5\n🔗 Meme: http://example.com/meme1",
                "2. Scream 2\n❤️ Reactions: 3\n🔗 Meme: http://example.com/meme2",
                "3. Scream 3\n❤️ Reactions: 4\n🔗 Meme: http://example.com/meme3"
            ]),
            reply_markup=None
        )

@pytest.mark.asyncio
async def test_handle_week_selection_no_screams():
    """
    Test that handle_week_selection sends a message indicating no data is available when there are no screams for the selected week.
    """
    mock_week_data = {"posts": []}
    
    with patch("app_bot.handlers.historyHandler.get_historical_week", return_value=mock_week_data):
        callback = AsyncMock(spec=CallbackQuery)
        callback.data = "week_2023-01"
        callback.answer = AsyncMock()
        callback.message = AsyncMock()
        
        await handle_week_selection(callback)

        callback.message.answer.assert_called_once_with("🚫 No data for the week 2023-01")

@pytest.mark.asyncio
async def test_handle_week_selection_error():
    """
    Test that handle_week_selection sends an error message when the API call fails.
    """
    
    with patch("app_bot.handlers.historyHandler.get_historical_week", side_effect=Exception("API Error")):
        callback = AsyncMock(spec=CallbackQuery)
        callback.data = "week_2023-01"
        callback.answer = AsyncMock()
        callback.message = AsyncMock()
        
        await handle_week_selection(callback)

        callback.message.answer.assert_called_once_with("❌ Error loading week data")
