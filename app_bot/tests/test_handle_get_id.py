import pytest
from aiogram import types
from unittest import mock
from app_bot.handlers.getIdHandler import handle_my_id


@pytest.mark.asyncio
async def test_handle_my_id_success():
    """
    Test that the handle_my_id function
    returns the correct user ID when the API call is successful.
    """

    mock_msg = mock.Mock(spec=types.Message)
    mock_msg.from_user = mock.Mock()
    mock_msg.from_user.id = 123456789
    mock_msg.answer = mock.AsyncMock()

    with mock.patch("app_bot.handlers.getIdHandler.get_my_id",
                    return_value={"user_id": "123456789"}):
        await handle_my_id(mock_msg)

    mock_msg.answer.assert_awaited_with("Your user_id: 123456789")


@pytest.mark.asyncio
async def test_handle_my_id_failure():
    """
    Test that the handle_my_id function
    handles failure when the API call raises an exception.
    """

    mock_msg = mock.Mock(spec=types.Message)
    mock_msg.from_user = mock.Mock()
    mock_msg.from_user.id = 123456789
    mock_msg.answer = mock.AsyncMock()

    with mock.patch("app_bot.handlers.getIdHandler.get_my_id",
                    side_effect=Exception("API error")):
        await handle_my_id(mock_msg)

    mock_msg.answer.assert_awaited_with("Failed to get user_id")
