
# Standard library
import hashlib

# Third‑party
import pytest

# Local application
from app_fastapi.tools.crypt import hash_user_id

def test_hash_raises_and_logs(monkeypatch, caplog):
    """
    If hashlib.sha256 throws, our function should log an error and re-raise.
    """
    class DummyError(Exception):
        pass

    def fake_sha256(_):
        raise DummyError("boom")

    monkeypatch.setattr(hashlib, "sha256", fake_sha256)
    caplog.set_level("ERROR", logger="app_fastapi.tools")

    with pytest.raises(DummyError):
        hash_user_id(123)

    assert "Failed to hash user ID" in caplog.text

def test_hash_output_length_and_type():
    """
    The hash of any input should be a 64-character hexadecimal string.
    """
    h = hash_user_id("user123")
    assert isinstance(h, str)
    assert len(h) == 64

    int(h, 16)

def test_hash_consistency():
    """
    The same input should always produce the same hash, different inputs differ.
    """
    assert hash_user_id("same") == hash_user_id("same")
    assert hash_user_id("diff1") != hash_user_id("diff2")

def test_hash_empty_string():
    """
    Hashing an empty string should still return a valid 64-character hex string.
    """
    h = hash_user_id("")
    assert isinstance(h, str)
    assert len(h) == 64