from app_fastapi.main import app
from app_fastapi.models.admin import Admin
from app_fastapi.tools.crypt import hash_user_id
from unittest.mock import patch
from .conftest import TestingSessionLocal


async def test_admin_middleware_valid(client):
    async with TestingSessionLocal() as session:
        admin = Admin(user_hash=hash_user_id("admin12345"))
        session.add(admin)
        await session.commit()

    json_data = {"user_id": "admin12345", "user_id_to_admin": "newadmin12345"}
    response = client.post("/create_admin", json=json_data)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_admin_middleware_invalid_json(client):
    response = client.post("/create_admin", data="Invalid JSON Data")
    assert response.status_code == 422
    assert "detail" in response.json()


async def test_admin_middleware_missing_user_id(client):
    response = client.post("/create_admin", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing user_id"}


async def test_admin_middleware_non_admin(client):
    json_data = {"user_id": "non_admin12345", "user_id_to_admin": "newadmin12345"}
    response = client.post("/create_admin", json=json_data)

    assert response.status_code == 403
    assert response.json() == {"detail": "Unauthorized: not an admin"}


async def test_create_admin_already_admin(client):
    json_data = {"user_id": "admin12345", "user_id_to_admin": "existingadmin12345"}
    response = client.post("/create_admin", json=json_data)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    json_data = {"user_id": "admin12345", "user_id_to_admin": "existingadmin12345"}
    response = client.post("/create_admin", json=json_data)

    assert response.status_code == 200
    assert response.json() == {"status": "already_admin"}


async def test_admin_middleware_general_error(client):
    with patch("app_fastapi.middlewares.admin.hash_user_id", side_effect=Exception("Unexpected Error")):
        json_data = {"user_id": "admin12345", "user_id_to_admin": "newadmin12345"}
        response = client.post("/create_admin", json=json_data)

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
