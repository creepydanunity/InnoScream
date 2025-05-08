import urllib.parse
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app_fastapi.main import app
from app_fastapi.models.scream import Scream
from app_fastapi.tests.conftest import TestingSessionLocal

client = TestClient(app)


async def test_get_weekly_stress_graph_all():
    now = datetime.now(timezone.utc).replace(
        hour=12, minute=0, second=0, microsecond=0
    )
    week_ago = now - timedelta(days=6)
    async with TestingSessionLocal() as session:
        for i in range(7):
            ts = week_ago + timedelta(days=i)
            scream = Scream(
                content=f"s{i}",
                user_hash=f"u{i}",
                timestamp=ts
            )
            session.add(scream)
        await session.commit()

    resp = client.get("/stress")
    assert resp.status_code == 200

    chart_url = resp.json()["chart_url"]
    decoded = urllib.parse.unquote(chart_url)

    expected_labels = [
        (week_ago + timedelta(days=i)).strftime("%a")
        for i in range(7)
    ]
    assert f"labels:{expected_labels}" in decoded
