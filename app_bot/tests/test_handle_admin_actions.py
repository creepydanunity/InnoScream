import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app_bot.handlers.adminHandler import (
    handle_delete,
    process_callback_button_back,
    process_callback_button_next,
    process_callback_button_exit,
    process_callback_button_delete,
    process_callback_button_confirm
)
from app_bot.FSM.admin import AdminScreamReview


@pytest.mark.asyncio
async def test_handle_delete_all_reviewed(monkeypatch):
    """Should notify admin if all screams are already reviewed (404)."""
    msg = MagicMock(spec=types.Message)
    msg.from_user = MagicMock()
    msg.from_user.id = 123
    msg.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)

    async def mock_get_all_screams_for_admin(_):
        raise httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404)
        )

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.get_all_screams_for_admin",
        mock_get_all_screams_for_admin
    )

    await handle_delete(msg, state)
    msg.answer.assert_called_once_with("🎉 All screams are already reviewed.")


@pytest.mark.asyncio
async def test_handle_delete_no_screams(monkeypatch):
    msg = MagicMock(spec=types.Message)
    msg.from_user = MagicMock()
    msg.from_user.id = 1
    msg.answer = AsyncMock()
    state = MagicMock(spec=FSMContext)

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.get_all_screams_for_admin",
        AsyncMock(return_value=[])
    )

    await handle_delete(msg, state)
    msg.answer.assert_awaited_with("😴 No screams available.")


@pytest.mark.asyncio
async def test_handle_delete_internal_error(monkeypatch):
    msg = MagicMock(spec=types.Message)
    msg.from_user = MagicMock()
    msg.from_user.id = 1
    msg.answer = AsyncMock()
    state = MagicMock(spec=FSMContext)

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.get_all_screams_for_admin",
        AsyncMock(return_value=[{"scream_id": 1, "content": "test"}])
    )
    state.update_data = AsyncMock(side_effect=Exception("fail"))

    await handle_delete(msg, state)
    msg.answer.assert_awaited_with("❌ Failed to start moderation")


@pytest.mark.asyncio
async def test_handle_delete_permission_denied(monkeypatch):
    """Should notify user they lack permission when HTTP 403 is raised."""
    msg = MagicMock(spec=types.Message)
    msg.from_user = MagicMock()
    msg.from_user.id = 123
    msg.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)

    mock_response = MagicMock(status_code=403)
    mock_request = MagicMock()

    async def mock_get_all_screams_for_admin(_):
        raise httpx.HTTPStatusError(
            "Forbidden",
            request=mock_request,
            response=mock_response
        )

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.get_all_screams_for_admin",
        mock_get_all_screams_for_admin
    )

    await handle_delete(msg, state)
    msg.answer.assert_awaited_once_with(
        "You do not have permission — only admins can perform this action."
    )


@pytest.mark.asyncio
async def test_handle_delete_displays_first_scream(monkeypatch):
    """Should update FSM state and display first scream to admin."""
    msg = MagicMock(spec=types.Message)
    msg.from_user = MagicMock()
    msg.from_user.id = 123
    msg.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()

    fake_screams = [{
        "scream_id": 111,
        "content": "Test scream content"
    }]

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.get_all_screams_for_admin",
        AsyncMock(return_value=fake_screams)
    )

    await handle_delete(msg, state)
    state.set_state.assert_awaited_once_with(AdminScreamReview.reviewing)

    called_args = msg.answer.call_args.kwargs["text"]
    assert all(x in called_args for x in
               ("Scream 1 out of 1", "111", "Test scream content")
               )


@pytest.mark.asyncio
async def test_process_callback_button_exit():
    """Should clear FSM state and confirm exit."""
    callback = MagicMock(spec=types.CallbackQuery)
    callback.from_user = MagicMock()
    callback.from_user.id = 456
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.clear = AsyncMock()

    await process_callback_button_exit(callback, state)
    state.clear.assert_awaited_once()
    callback.message.edit_text.assert_awaited_once_with(
        "🚪 Exited moderation mode.",
        reply_markup=None
    )


@pytest.mark.asyncio
async def test_process_callback_button_exit_fail():
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.from_user.id = 6
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock(side_effect=Exception("boom"))
    callback.answer = AsyncMock()
    state = MagicMock(spec=FSMContext)
    state.clear = AsyncMock()

    await process_callback_button_exit(callback, state)
    callback.answer.assert_awaited_with("❌ Exit failed")


@pytest.mark.asyncio
async def test_process_callback_button_back():
    """Should go to previous scream and update message."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()
    callback.data = "button_back"

    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={
        "index": 1,
        "screams": [
            {"scream_id": 111, "content": "first"},
            {"scream_id": 222, "content": "second"}
        ]
    })
    state.update_data = AsyncMock()

    await process_callback_button_back(callback, state)
    callback.message.edit_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_callback_button_next():
    """Should go to next scream and update message."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()
    callback.data = "button_next"

    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={
        "index": 0,
        "screams": [
            {"scream_id": 111, "content": "first"},
            {"scream_id": 222, "content": "second"}
        ]
    })
    state.update_data = AsyncMock()

    await process_callback_button_next(callback, state)
    callback.message.edit_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_callback_button_next_exception():
    """Should handle unexpected exceptions during 'next' navigation."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.from_user.id = 123
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()
    callback.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(side_effect=Exception(
        "unexpected navigation failure"
    ))

    await process_callback_button_next(callback, state)
    callback.answer.assert_awaited_once_with("❌ Navigation error")
    callback.message.edit_text.assert_not_awaited()


@pytest.mark.asyncio
async def test_process_callback_button_delete(monkeypatch):
    """Should delete scream and show next one."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.message = MagicMock()
    callback.from_user.id = 123
    callback.message.edit_text = AsyncMock()
    callback.message.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={
        "index": 0,
        "screams": [
            {"scream_id": 111, "content": "hello"},
            {"scream_id": 222, "content": "world"}
        ]
    })
    state.update_data = AsyncMock()
    state.clear = AsyncMock()

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.delete_scream",
        AsyncMock(return_value={"status": "deleted"})
    )

    await process_callback_button_delete(callback, state)
    callback.message.edit_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_callback_button_delete_fail(monkeypatch):
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.from_user.id = 4
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()
    callback.message.answer = AsyncMock()
    callback.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={
        "index": 0,
        "screams": [{"scream_id": 1, "content": "abc"}]
    })

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.delete_scream",
        AsyncMock(return_value={"status": "failed"})
    )

    await process_callback_button_delete(callback, state)
    callback.message.answer.assert_awaited_with("🤔 Couldn't delete scream.")


@pytest.mark.asyncio
async def test_process_callback_button_delete_all_reviewed(monkeypatch):
    """Should clear state when all screams are reviewed after deletion."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.from_user.id = 123
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()
    callback.message.answer = AsyncMock()
    callback.answer = AsyncMock()

    initial_screams = [{"scream_id": 999, "content": "lonely scream"}]
    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={
        "index": 0,
        "screams": initial_screams
    })
    state.clear = AsyncMock()
    state.update_data = AsyncMock()

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.delete_scream",
        AsyncMock(return_value={"status": "deleted"})
    )

    await process_callback_button_delete(callback, state)
    callback.message.answer.assert_awaited_once_with("✅ All screams reviewed.")
    state.clear.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_callback_button_delete_exception(monkeypatch):
    """Should handle exceptions during deletion with error message."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.from_user.id = 123
    callback.message = MagicMock()
    callback.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={
        "index": 0,
        "screams": [{"scream_id": 555, "content": "test scream"}]
    })

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.delete_scream",
        AsyncMock(side_effect=Exception("DB unreachable"))
    )

    await process_callback_button_delete(callback, state)
    callback.answer.assert_awaited_once_with("❌ Deletion failed")


@pytest.mark.asyncio
async def test_process_callback_button_confirm(monkeypatch):
    """Should confirm scream and show next one."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.message = MagicMock()
    callback.from_user.id = 321
    callback.message.edit_text = AsyncMock()
    callback.message.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={
        "index": 0,
        "screams": [
            {"scream_id": 333, "content": "confirmed"},
            {"scream_id": 444, "content": "next"}
        ]
    })
    state.update_data = AsyncMock()
    state.clear = AsyncMock()

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.confirm_scream",
        AsyncMock(return_value={"status": "confirmed"})
    )

    await process_callback_button_confirm(callback, state)
    callback.message.edit_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_callback_button_confirm_fail(monkeypatch):
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.from_user.id = 5
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()
    callback.message.answer = AsyncMock()
    callback.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={
        "index": 0,
        "screams": [{"scream_id": 2, "content": "abc"}]
    })

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.confirm_scream",
        AsyncMock(return_value={"status": "error"})
    )

    await process_callback_button_confirm(callback, state)
    callback.message.answer.assert_awaited_with("🤔 Could not confirm scream.")


@pytest.mark.asyncio
async def test_process_callback_button_confirm_all_reviewed(monkeypatch):
    """Should clear state when all screams are confirmed."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.from_user.id = 999
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()
    callback.message.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={
        "index": 0,
        "screams": [{"scream_id": 101, "content": "last scream"}]
    })
    state.clear = AsyncMock()
    state.update_data = AsyncMock()

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.confirm_scream",
        AsyncMock(return_value={"status": "confirmed"})
    )

    await process_callback_button_confirm(callback, state)
    callback.message.answer.assert_awaited_once_with("🎉 All screams reviewed.")
    state.clear.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_callback_button_confirm_failed(monkeypatch):
    """Should notify user if confirmation fails (status != 'confirmed')."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.from_user.id = 123
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()
    callback.message.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={
        "index": 0,
        "screams": [{"scream_id": 999, "content": "broken scream"}]
    })
    state.update_data = AsyncMock()

    monkeypatch.setattr(
        "app_bot.handlers.adminHandler.confirm_scream",
        AsyncMock(return_value={"status": "error"})
    )

    await process_callback_button_confirm(callback, state)
    callback.message.answer.assert_awaited_once_with(
        "🤔 Could not confirm scream."
        )


@pytest.mark.asyncio
async def test_process_callback_button_confirm_exception(monkeypatch):
    """Should handle unexpected exceptions during confirmation."""
    callback = MagicMock(spec=CallbackQuery)
    callback.from_user = MagicMock()
    callback.from_user.id = 123
    callback.message = MagicMock()
    callback.message.edit_text = AsyncMock()
    callback.message.answer = AsyncMock()
    callback.answer = AsyncMock()

    state = MagicMock(spec=FSMContext)
    state.get_data = AsyncMock(side_effect=Exception("unexpected failure"))

    await process_callback_button_confirm(callback, state)
    callback.answer.assert_awaited_once_with("❌ Confirmation failed")
    callback.message.edit_text.assert_not_awaited()
