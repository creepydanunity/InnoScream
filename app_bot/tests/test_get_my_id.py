import pytest
from unittest.mock import patch, MagicMock
import httpx
from app_bot.api.api import get_my_id

@pytest.mark.asyncio
async def test_get_my_id_success():
    mock_response = {"user_id": "123456"}
    
    with patch.object(httpx.AsyncClient, 'post', return_value=MagicMock(status_code=200, json=lambda: mock_response)):
        result = await get_my_id("123456")
        
        assert result == mock_response
        assert result["user_id"] == "123456"


@pytest.mark.asyncio
async def test_get_my_id_failure():
    mock_response = MagicMock(status_code=500)
    mock_request = MagicMock()
    with patch.object(httpx.AsyncClient, 'post', side_effect=httpx.HTTPStatusError("Failed request", request=mock_request, response=mock_response)):
        with pytest.raises(httpx.HTTPStatusError):
            await get_my_id("123456")
