# Standard library
from datetime import datetime as real_datetime, timedelta, timezone

# Third‑party
import pytest

# Local application
import app_fastapi.tools.time as time_module
from app_fastapi.tools.time import get_bounds, get_week_start

class FakeDateTime(real_datetime):
    """
    Subclass of datetime.datetime to override now().
    """
    @classmethod
    def now(cls, tz=None):
        return cls._fixed_now

_original_module_datetime = time_module.datetime
_original_fake_now = FakeDateTime.now

@pytest.fixture(autouse=True)
def reset_module_datetime(monkeypatch):
    """
    Restore original datetime and FakeDateTime.now after each test.
    """
    yield
    monkeypatch.setattr(time_module, "datetime", _original_module_datetime)
    FakeDateTime.now = _original_fake_now

def test_get_bounds_addition_true(monkeypatch):
    """
    get_bounds should return today’s midnight and midnight plus days when addition=True.
    """
    fixed = real_datetime(2025, 5, 3, 15, 30, tzinfo=timezone.utc)
    FakeDateTime._fixed_now = fixed
    monkeypatch.setattr(time_module, "datetime", FakeDateTime)

    start, end = get_bounds(days=2, addition=True)
    expected_start = real_datetime(2025, 5, 3, 0, 0, tzinfo=timezone.utc)
    expected_end = expected_start + timedelta(days=2)
    assert start == expected_start
    assert end == expected_end

def test_get_bounds_addition_false(monkeypatch):
    """
    get_bounds should return today’s midnight and midnight minus days when addition=False.
    """
    fixed = real_datetime(2025, 5, 3, 9, 0, tzinfo=timezone.utc)
    FakeDateTime._fixed_now = fixed
    monkeypatch.setattr(time_module, "datetime", FakeDateTime)

    start, end = get_bounds(days=5, addition=False)
    expected_start = real_datetime(2025, 5, 3, 0, 0, tzinfo=timezone.utc)
    expected_end = expected_start - timedelta(days=5)
    assert start == expected_start
    assert end == expected_end

def test_get_bounds_exception(monkeypatch, caplog):
    """
    get_bounds should log an error and re‑raise if datetime.now() fails.
    """
    class Boom(Exception):
        pass

    def boom_now(cls, tz=None):
        raise Boom("fail")

    FakeDateTime.now = classmethod(boom_now)
    monkeypatch.setattr(time_module, "datetime", FakeDateTime)
    caplog.set_level("ERROR", logger="app_fastapi.tools")

    with pytest.raises(Boom):
        get_bounds()

    assert "Failed to calculate time bounds" in caplog.text

def test_get_week_start_monday(monkeypatch):
    """
    get_week_start should return Monday midnight when today is mid‑week.
    """
    fixed = real_datetime(2025, 5, 7, 14, 0, tzinfo=timezone.utc)
    FakeDateTime._fixed_now = fixed
    monkeypatch.setattr(time_module, "datetime", FakeDateTime)

    ws = get_week_start()
    assert ws == real_datetime(2025, 5, 5, 0, 0, tzinfo=timezone.utc)

@pytest.mark.parametrize("weekday, expected_date", [
    (0, "2025-05-05"),
    (6, "2025-05-05"),
])
def test_get_week_start_various(monkeypatch, weekday, expected_date):
    """
    get_week_start should always roll back to the Monday of the current week.
    """
    base = real_datetime(2025, 5, 5, tzinfo=timezone.utc)
    fixed = base + timedelta(days=weekday, hours=18)
    FakeDateTime._fixed_now = fixed
    monkeypatch.setattr(time_module, "datetime", FakeDateTime)

    ws = get_week_start()
    assert ws.date().isoformat() == expected_date
    assert (ws.hour, ws.minute, ws.second) == (0, 0, 0)