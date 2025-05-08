import pytest
import httpx
from unittest.mock import patch, MagicMock

from app_bot.api.api import archive_current_week


@pytest.mark.asyncio
async def test_archive_current_week_success():
    """
    Should successfully archive the current week and return confirmation JSON.
    """
    week_id = "2025-18"
    user_id = "admin123"
    mock_json = {"status": "archived", "count": 3}

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json = lambda: mock_json
    mock_response.raise_for_status = MagicMock()

    with patch.object(httpx.AsyncClient, 'post', return_value=mock_response):
        result = await archive_current_week(week_id, user_id)
        assert result == mock_json


@pytest.mark.asyncio
async def test_archive_current_week_already_exists():
    """
    Should raise ValueError if the archive already exists (HTTP 409).
    """
    week_id = "2025-18"
    user_id = "admin123"

    mock_response = MagicMock(status_code=409)
    mock_request = MagicMock()
    exception = httpx.HTTPStatusError(
        "Conflict",
        request=mock_request,
        response=mock_response)

    with patch.object(httpx.AsyncClient, 'post', side_effect=exception):
        with pytest.raises(ValueError, match="Week already archived"):
            await archive_current_week(week_id, user_id)


@pytest.mark.asyncio
async def test_archive_current_week_other_http_error():
    """
    Should re-raise HTTPStatusError for errors other than 409.
    """
    week_id = "2025-18"
    user_id = "admin123"

    mock_response = MagicMock(status_code=500)
    mock_request = MagicMock()
    exception = httpx.HTTPStatusError(
        "Server Error",
        request=mock_request,
        response=mock_response)

    with patch.object(httpx.AsyncClient, 'post', side_effect=exception):
        with pytest.raises(httpx.HTTPStatusError):
            await archive_current_week(week_id, user_id)


@pytest.mark.asyncio
async def test_archive_current_week_generic_exception():
    """
    Should catch and re-raise unexpected exceptions.
    """
    week_id = "2025-18"
    user_id = "admin123"

    with patch.object(
        httpx.AsyncClient,
        'post',
        side_effect=Exception("unexpected error")
    ):
        with pytest.raises(Exception, match="unexpected error"):
            await archive_current_week(week_id, user_id)
