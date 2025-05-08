# Standard library
from datetime import datetime, timezone

# Third‑party
import pytest

# Local application
from app_fastapi.models.reaction import Reaction


@pytest.fixture
def example_reaction():
    """
    Create a Reaction instance with fixed attributes for repr/str testing.
    """
    r = Reaction(emoji="🔥", scream_id=7, user_hash="deadbeef")
    r.id = 99
    r.timestamp = datetime(2025, 1, 1, tzinfo=timezone.utc)
    return r


def test_repr_includes_emoji_and_scream_id(example_reaction, caplog):
    """
    __repr__ should show the emoji and the scream_id.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.models")

    s = repr(example_reaction)
    assert s == "<Reaction(🔥) on Scream 7>"


def test_str_shows_id_and_emoji(example_reaction, caplog):
    """
    __str__ should show both the id and the emoji.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.models")

    s = str(example_reaction)
    assert s == "Reaction(id=99, emoji=🔥)"
