import pytest
from unittest.mock import patch, MagicMock
import httpx
from app_bot.api.api import get_all_screams_for_admin

@pytest.mark.asyncio
async def test_get_all_screams_for_admin_success():
    """
    Should return list of screams when admin fetch is successful.
    """
    mock_response = {
        "posts": [
            {"scream_id": 1, "content": "First scream"},
            {"scream_id": 2, "content": "Second scream"},
        ]
    }

    with patch.object(
        httpx.AsyncClient, "post", return_value=MagicMock(status_code=200, json=lambda: mock_response)
    ):
        result = await get_all_screams_for_admin("admin_001")

        assert result == mock_response
        assert len(result["posts"]) == 2
        assert result["posts"][0]["scream_id"] == 1

@pytest.mark.asyncio
async def test_get_all_screams_for_admin_failure():
    """
    Should raise HTTPStatusError when API call fails.
    """
    mock_response = MagicMock(status_code=500)
    mock_request = MagicMock()

    with patch.object(
        httpx.AsyncClient, "post",
        side_effect=httpx.HTTPStatusError("Request failed", request=mock_request, response=mock_response)
    ):
        with pytest.raises(httpx.HTTPStatusError):
            await get_all_screams_for_admin("admin_001")
