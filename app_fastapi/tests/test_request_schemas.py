# Standard library
import logging

# Third‑party
import pytest
from pydantic import ValidationError

# Local application
from app_fastapi.schemas.requests import (
    CreateScreamRequest,
    CreateAdminRequest,
    GetIdRequest,
    ReactionRequest,
    DeleteRequest,
    UserRequest,
)

logger = logging.getLogger("app_fastapi.schemas")


@pytest.mark.parametrize("content,user_id", [
    ("hello", "user1"),
    ("x" * 280, "u"),
])
def test_create_scream_request_valid(caplog, content, user_id):
    """
    CreateScreamRequest should accept valid content lengths and user IDs.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    req = CreateScreamRequest(content=content, user_id=user_id)
    # repr should include abbreviated user_id
    r = repr(req)
    assert "<CreateScreamRequest(user=" in r
    assert user_id[:5] in r


def test_create_admin_request_and_repr(caplog):
    """
    CreateAdminRequest should store both IDs and its repr abbreviates them.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    req = CreateAdminRequest(user_id="requester123", user_id_to_admin="target456")
    assert req.user_id == "requester123"
    assert req.user_id_to_admin == "target456"
    r = repr(req)
    assert "<CreateAdminRequest(from=" in r and "to=" in r


def test_get_id_request_and_missing(caplog):
    """
    GetIdRequest should require a non-empty user_id, repr abbreviates it.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    req = GetIdRequest(user_id="xyz")
    assert repr(req).startswith("<GetIdRequest")
    with pytest.raises(ValidationError):
        GetIdRequest(user_id=None)


def test_reaction_request_and_repr(caplog):
    """
    ReactionRequest should require scream_id, emoji, user_id; repr abbreviates user_id.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    req = ReactionRequest(scream_id=5, emoji="👍", user_id="reactorXYZ")
    assert req.scream_id == 5
    assert req.emoji == "👍"
    assert "<ReactionRequest(user=" in repr(req)


def test_delete_request_and_repr(caplog):
    """
    DeleteRequest should require scream_id and user_id; repr abbreviates user_id.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    req = DeleteRequest(scream_id=42, user_id="deleterABC")
    assert req.scream_id == 42
    assert "<DeleteRequest(user=" in repr(req)


def test_user_request_and_repr(caplog):
    """
    UserRequest should require user_id; repr abbreviates user_id.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    req = UserRequest(user_id="somebody")
    assert req.user_id == "somebody"
    assert "<UserRequest(user=" in repr(req)
