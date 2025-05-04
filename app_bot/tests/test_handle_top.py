import pytest
from unittest.mock import AsyncMock, MagicMock

from app_bot.handlers.screamHandler import handle_top


@pytest.mark.asyncio
async def test_handle_top_no_posts(monkeypatch):
    """
    Test the /top command when no top screams are returned.

    Steps:
    - Mocks get_top_screams to return an empty list of posts.
    - Verifies that the bot replies with a "no top screams" message.
    """
    msg = MagicMock()
    msg.answer = AsyncMock()
    msg.answer_photo = AsyncMock()

    monkeypatch.setattr(
        "app_bot.handlers.screamHandler.get_top_screams",
        AsyncMock(return_value={"posts": []})
    )

    await handle_top(msg)
    msg.answer.assert_awaited_once_with("😴 No top screams today...")


@pytest.mark.asyncio
async def test_handle_top_with_and_without_meme(monkeypatch):
    """
    Test the /top command with a mix of screams:
    - One with a meme image URL.
    - One without a meme.

    Verifies:
    - First scream sends an image with caption via answer_photo.
    - Second scream sends a plain message via answer.
    """
    msg = MagicMock()
    msg.answer = AsyncMock()
    msg.answer_photo = AsyncMock()

    posts = [
        {"content": "Hello world", "votes": 1, "meme_url": "http://img/1.jpg"},
        {"content": "Foo bar",    "votes": 2},
    ]
    monkeypatch.setattr(
        "app_bot.handlers.screamHandler.get_top_screams",
        AsyncMock(return_value={"posts": posts})
    )

    await handle_top(msg)

    caption1 = (
        "🔥 <b>Top scream #1</b>\n"
        "🗯️ <i>Hello world</i>\n"
        "👍 <b>1</b> vote"
    )
    msg.answer_photo.assert_awaited_once_with(
        photo="http://img/1.jpg",
        caption=caption1,
        parse_mode="HTML"
    )

    caption2 = (
        "🔥 <b>Top scream #2</b>\n"
        "🗯️ <i>Foo bar</i>\n"
        "👍 <b>2</b> votes"
    )
    msg.answer.assert_awaited_with(caption2, parse_mode="HTML")


@pytest.mark.asyncio
async def test_handle_top_raises(monkeypatch, caplog):
    """
    Test the /top command when get_top_screams raises an error.

    Steps:
    - Mocks get_top_screams to raise RuntimeError.
    - Verifies the bot replies with an error message.
    - Asserts the error is logged correctly.
    """
    msg = MagicMock()
    msg.answer = AsyncMock()
    msg.answer_photo = AsyncMock()

    async def boom():
        raise RuntimeError("nope")
    monkeypatch.setattr(
        "app_bot.handlers.screamHandler.get_top_screams",
        boom
    )

    await handle_top(msg)
    msg.answer.assert_awaited_with("😴 There was an error getting top screams((")
    assert "Failed to get top screams: nope" in caplog.text
