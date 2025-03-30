import pytest_asyncio
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.conftest import get_test_db_client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_expenses_collection():
    client = await get_test_db_client()
    db = client[settings.TEST_DB_NAME]
    await db["expenses"].delete_many({})


def test_create_expense(client: TestClient, auth_headers: dict):
    response = client.post(
        "/expenses/",
        json={"amount": 100, "description": "Test expense"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 100
    assert data["description"] == "Test expense"


def test_get_expenses(client: TestClient, auth_headers: dict):
    response = client.get("/expenses/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_get_expense(client: TestClient, auth_headers: dict):
    response = client.post(
        "/expenses/",
        json={"amount": 100, "description": "Test expense"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    expense_id = data["id"]

    response = client.get(f"/expenses/{expense_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == expense_id
    assert data["amount"] == 100
    assert data["description"] == "Test expense"
