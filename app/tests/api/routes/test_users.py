from uuid import uuid4

import pytest_asyncio
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.conftest import get_test_db_client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_users_collection():
    client = await get_test_db_client()
    db = client[settings.TEST_DB_NAME]
    await db["users"].delete_many({})


def test_test_auth(client: TestClient, auth_headers: dict):
    response = client.get("/users/test-auth", headers=auth_headers)
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
