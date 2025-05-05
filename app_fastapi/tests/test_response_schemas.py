# Standard library
import logging

# Local application
from app_fastapi.schemas.responses import (
    CreateScreamResponse,
    CreateAdminResponse,
    GetMyIdResponse,
    ReactionResponse,
    TopScreamItem,
    TopScreamsResponse,
    ArchivedWeeksResponse,
    UserStatsResponse,
    DeleteResponse,
    StressStatsResponse,
    ScreamResponse,
)

logger = logging.getLogger("app_fastapi.schemas")


def test_create_scream_response_repr(caplog):
    """
    CreateScreamResponse __repr__ should include status and scream_id.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    r = CreateScreamResponse(status="ok", scream_id=7)
    text = repr(r)
    assert text == "<CreateScreamResponse(status=ok, scream_id=7)>"
    assert "CreateScreamResponse representation" in caplog.text


def test_create_admin_response_and_repr(caplog):
    """
    CreateAdminResponse should store status and repr it.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    r = CreateAdminResponse(status="already_admin")
    assert r.status == "already_admin"
    assert repr(r) == "<CreateAdminResponse(status=already_admin)>"


def test_get_my_id_response_repr(caplog):
    """
    GetMyIdResponse __repr__ abbreviates the user_id.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    r = GetMyIdResponse(user_id="abcdefghijkl")
    text = repr(r)
    assert text.startswith("<GetMyIdResponse(user=abcde")
    assert "GetMyIdResponse representation" in caplog.text


def test_reaction_response_repr(caplog):
    """
    ReactionResponse repr includes status.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    r = ReactionResponse(status="ok")
    assert repr(r) == "<ReactionResponse(status=ok)>"


def test_top_scream_item_and_repr(caplog):
    """
    TopScreamItem __repr__ shows id and votes.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    item = TopScreamItem(id=1, content="c", votes=5, meme_url="u")
    assert repr(item) == "<TopScreamItem(id=1, votes=5)>"


def test_top_screams_response_and_repr(caplog):
    """
    TopScreamsResponse repr shows number of posts.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    items = [TopScreamItem(id=i,
                           content="",
                           votes=0,
                           meme_url="") for i in range(3)]
    resp = TopScreamsResponse(posts=items)
    assert repr(resp) == "<TopScreamsResponse(posts=3)>"


def test_archived_weeks_response():
    """
    ArchivedWeeksResponse should hold weeks list.
    """
    resp = ArchivedWeeksResponse(weeks=[2025, 2024])
    assert resp.weeks == [2025, 2024]


def test_user_stats_response_repr(caplog):
    """
    UserStatsResponse repr includes screams_posted and reactions_got.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    r = UserStatsResponse(
        screams_posted=10,
        reactions_given=3,
        reactions_got=7,
        chart_url="cu",
        reaction_chart_url="cr"
    )
    assert "<UserStatsResponse(screams=10, reactions=7)>" == repr(r)


def test_delete_response_repr(caplog):
    """
    DeleteResponse repr includes status.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    r = DeleteResponse(status="deleted")
    assert repr(r) == "<DeleteResponse(status=deleted)>"


def test_stress_stats_response_repr(caplog):
    """
    StressStatsResponse repr is fixed.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    r = StressStatsResponse(chart_url="xx")
    assert repr(r) == "<StressStatsResponse>"


def test_scream_response_repr(caplog):
    """
    ScreamResponse repr shows scream_id.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.schemas")
    r = ScreamResponse(scream_id=99, content="hello")
    assert repr(r) == "<ScreamResponse(scream_id=99)>"
