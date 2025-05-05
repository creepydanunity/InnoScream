import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import patch

from app_fastapi.main import app

client = TestClient(app)

def test_get_my_id_success():
    resp = client.post("/my_id", json={"user_id": "abcdef12345"})
    assert resp.status_code == 200
    assert resp.json() == {"user_id": "abcdef12345"}

def test_get_my_id_missing_user_id():
    # Empty string triggers our 400 path
    resp = client.post("/my_id", json={"user_id": ""})
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Missing user_id"}

def test_get_my_id_invalid_payload():
    # no user_id key → pydantic validation error 422
    resp = client.post("/my_id", json={"foo": "bar"})
    assert resp.status_code == 422
    # Should include mention of "user_id"
    body = resp.json()
    errors = body.get("detail", [])
    assert any(err.get("loc", [])[-1] == "user_id" for err in errors)

def test_get_my_id_unexpected_error(monkeypatch):
    # Force an exception in the handler by monkey‑patching logger.debug
    def boom(_):
        raise RuntimeError("boom")
    monkeypatch.setattr("app_fastapi.api.endpoints.logger.debug", boom)

    resp = client.post("/my_id", json={"user_id": "abc"})
    assert resp.status_code == 500
    assert resp.json() == {"detail": "Internal server error"}
