import pytest, httpx
from unittest import mock
from unittest.mock import patch, AsyncMock
from aiogram import types
from app_bot.handlers.adminHandler import handle_create_admin
from app_bot.api.api import create_admin
from app_bot.logger import logger 

@pytest.mark.asyncio
async def test_handle_create_admin_success():
    mock_response = {"status": "ok"}
    
    mock_msg = mock.Mock(spec=types.Message)
    mock_msg.text = "/create_admin 12345"
    mock_msg.from_user = mock.Mock()
    mock_msg.from_user.id = 67890
    mock_msg.answer = AsyncMock()

    with patch("app_bot.handlers.adminHandler.logger") as mock_logger:

        with patch("app_bot.handlers.adminHandler.create_admin", return_value=mock_response):
            await handle_create_admin(mock_msg)

        mock_msg.answer.assert_awaited_with("User 12345 is now an admin!")

        mock_logger.info.assert_any_call("Successfully created admin 12345")


@pytest.mark.asyncio
async def test_handle_create_admin_already_admin():
    mock_response = {"status": "already_admin"}
    
    mock_msg = mock.Mock(spec=types.Message)
    mock_msg.text = "/create_admin 12345"
    mock_msg.from_user = mock.Mock
    mock_msg.from_user.id = 67890
    mock_msg.answer = AsyncMock()

    with patch("app_bot.handlers.adminHandler.logger") as mock_logger:
            
        with patch("app_bot.handlers.adminHandler.create_admin", return_value=mock_response):
            await handle_create_admin(mock_msg)

        mock_msg.answer.assert_awaited_with("This user is already an admin.")
        
        mock_logger.info.assert_any_call("User 12345 is already admin")

@pytest.mark.asyncio
async def test_handle_create_admin_invalid_format():
    mock_msg = mock.Mock(spec=types.Message)
    mock_msg.text = "/create_admin"
    mock_msg.from_user = mock.Mock
    mock_msg.from_user.id = 67890
    mock_msg.answer = AsyncMock()

    await handle_create_admin(mock_msg)

    mock_msg.answer.assert_awaited_with("Usage: /create_admin <user_id>")

    with patch("app_bot.handlers.adminHandler.logger") as mock_logger:
        await handle_create_admin(mock_msg)

        mock_msg.answer.assert_awaited_with("Usage: /create_admin <user_id>")

        mock_logger.warning.assert_any_call("Invalid create_admin command format from user 67890")

@pytest.mark.asyncio
async def test_handle_create_admin_permission_denied():
    mock_response = mock.Mock(status_code=403)
    
    mock_msg = mock.Mock(spec=types.Message)
    mock_msg.text = "/create_admin 12345"
    mock_msg.from_user = mock.Mock()
    mock_msg.from_user.id = 67890
    mock_msg.answer = AsyncMock()

    with patch("app_bot.handlers.adminHandler.create_admin", side_effect=httpx.HTTPStatusError("Permission denied", request=mock.Mock(), response=mock_response)):
        
        with patch("app_bot.handlers.adminHandler.logger") as mock_logger:
            await handle_create_admin(mock_msg)

            mock_msg.answer.assert_awaited_with("You do not have permission — only admins can perform this action.")

            mock_logger.warning.assert_any_call("Permission denied for user 67890")


@pytest.mark.asyncio
async def test_handle_create_admin_server_error():
    mock_response = mock.Mock(status_code=500)
    
    mock_msg = mock.Mock(spec=types.Message)
    mock_msg.text = "/create_admin 12345"
    mock_msg.from_user = mock.Mock()
    mock_msg.from_user.id = 67890
    mock_msg.answer = AsyncMock()

    with patch("app_bot.handlers.adminHandler.create_admin", side_effect=httpx.HTTPStatusError("Server error", request=mock.Mock(), response=mock_response)):
        with patch("app_bot.handlers.adminHandler.logger") as mock_logger:

            await handle_create_admin(mock_msg)

            mock_msg.answer.assert_awaited_with("Server error occurred.")

            mock_logger.error.assert_any_call("HTTP error in create_admin: Server error", exc_info=True)

@pytest.mark.asyncio
async def test_handle_create_admin_exception():
    mock_msg = mock.Mock(spec=types.Message)
    mock_msg.text = "/create_admin 12345"
    mock_msg.from_user = mock.Mock
    mock_msg.from_user.id = 67890
    mock_msg.answer = AsyncMock()

    with patch("app_bot.handlers.adminHandler.create_admin", side_effect=Exception("Unexpected error")):
        with patch("app_bot.handlers.adminHandler.logger") as mock_logger:

            await handle_create_admin(mock_msg)

            mock_msg.answer.assert_awaited_with("Failed to assign admin rights.")

            mock_logger.error.assert_any_call("Failed to assign admin rights: Unexpected error", exc_info=True)
