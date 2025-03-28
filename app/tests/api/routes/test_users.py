from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


@pytest.fixture(scope="function", autouse=True)
async def clean_users_collection(db: AsyncIOMotorClient):
    test_db_name = settings.MONGODB_DB + "_test"
    await db[test_db_name]["users"].delete_many({})
    yield


def test_test_auth(client: TestClient, auth_headers: dict):
    response = client.get(
        "/users/test-auth", headers=auth_headers
    )
    assert response.status_code == 200


def test_create_user(client: TestClient):
    user_id = str(uuid4())
    response = client.post("/users/", json={"id": user_id, "expense_ids": []})

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["expense_ids"] == []


def test_create_duplicate_user(client: TestClient):
    user_id = str(uuid4())
    response = client.post("/users/", json={"id": user_id, "expense_ids": []})
    assert response.status_code == 200

    response = client.post("/users/", json={"id": user_id, "expense_ids": []})
    assert response.status_code == 400


def test_delete_user(client: TestClient):
    user_id = str(uuid4())
    response = client.post("/users/", json={"id": user_id, "expense_ids": []})
    assert response.status_code == 200

    response = client.delete(f"/users/?id={user_id}")
    assert response.status_code == 200

    response = client.delete(f"/users/?id={user_id}")
    assert response.status_code == 404


def test_delete_nonexistent_user(client: TestClient):
    non_existent_id = str(uuid4())
    response = client.delete(f"/users/?id={non_existent_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "user not found"
