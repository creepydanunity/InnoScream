# Standard library
from datetime import datetime, timezone

# Third‑party
import pytest

# Local application
from app_fastapi.models.scream import Scream

@pytest.fixture
def example_scream():
    """
    Return a Scream instance with known values for id, content, and user_hash.
    """
    s = Scream(content="This is a test scream content", user_hash="abcdef123456")

    s.id = 99
    s.timestamp = datetime(2025, 1, 1, tzinfo=timezone.utc)
    return s

def test_str(example_scream, caplog):
    """
    __str__ should be 'Scream(id=<id>)'.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.models")

    s = str(example_scream)
    assert s == "Scream(id=99)"
    assert "Scream string representation" in caplog.text

def test_repr(example_scream, caplog):
    """
    __repr__ should include id, truncated content, and user hash prefix;
    """
    caplog.set_level("DEBUG", logger="app_fastapi.models")

    s = repr(example_scream)
    assert s.startswith("<Scream(id=99,")
    assert "Scream representation" in caplog.text
