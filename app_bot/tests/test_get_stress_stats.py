import pytest
from unittest.mock import patch, MagicMock
import httpx
from app_bot.api.api import get_stress_stats


@pytest.mark.asyncio
async def test_get_stress_stats_success():
    """
    Should return stress chart data when API call succeeds.
    """
    mock_response = {"chart_url": "https://example.com/chart.png"}

    with patch.object(
        httpx.AsyncClient, "get", return_value=MagicMock(
            status_code=200, json=lambda: mock_response
            )
    ):
        result = await get_stress_stats()

        assert result == mock_response
        assert "chart_url" in result


@pytest.mark.asyncio
async def test_get_stress_stats_failure():
    """
    Should raise HTTPStatusError when the backend returns an error.
    """
    mock_response = MagicMock(status_code=500)
    mock_request = MagicMock()

    with patch.object(
        httpx.AsyncClient, "get",
        side_effect=httpx.HTTPStatusError(
            "Request failed", request=mock_request, response=mock_response
            )
    ):
        with pytest.raises(httpx.HTTPStatusError):
            await get_stress_stats()
