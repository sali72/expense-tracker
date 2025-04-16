from uuid import uuid4

import pytest_asyncio
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.E2E.conftest import get_test_db_client


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
    assert data["count"] == 0
    assert len(data["data"]) == 0


def test_get_expenses_with_expenses(client: TestClient, auth_headers: dict):
    response = client.post(
        "/expenses/",
        json={"amount": 100, "description": "Test expense"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    expense_id = data["id"]

    response = client.get("/expenses/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == expense_id


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


def test_get_nonexistent_expense(client: TestClient, auth_headers: dict):
    response = client.get(f"/expenses/{str(uuid4())}", headers=auth_headers)
    assert response.status_code == 404


def test_update_expense(client: TestClient, auth_headers: dict):
    response = client.post(
        "/expenses/",
        json={"amount": 100, "description": "Test expense"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    expense_id = data["id"]

    response = client.patch(
        f"/expenses/{expense_id}",
        json={"amount": 200, "description": "Updated expense"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == expense_id
    assert data["amount"] == 200
    assert data["description"] == "Updated expense"


def test_update_nonexistent_expense(client: TestClient, auth_headers: dict):
    url = f"/expenses/{str(uuid4())}"

    response = client.patch(
        url,
        json={"amount": 200},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_delete_expense(client: TestClient, auth_headers: dict):
    response = client.post(
        "/expenses/",
        json={"amount": 100, "description": "Test expense"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    expense_id = data["id"]

    response = client.delete(f"/expenses/{expense_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == expense_id


def test_delete_nonexistent_expense(client: TestClient, auth_headers: dict):
    response = client.delete(f"/expenses/{str(uuid4())}", headers=auth_headers)
    assert response.status_code == 404


def test_get_expenses_pagination(client: TestClient, auth_headers: dict):
    # Create 15 expenses
    expense_ids = []
    for i in range(15):
        response = client.post(
            "/expenses/",
            json={"amount": 100 + i, "description": f"Test expense {i}"},
            headers=auth_headers,
        )
        expense_ids.append(response.json()["id"])
    
    # Test first page with 10 items
    response = client.get("/expenses/?skip=0&limit=10", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 15
    assert len(data["data"]) == 10
    
    # Test second page with 5 items
    response = client.get("/expenses/?skip=10&limit=10", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 15
    assert len(data["data"]) == 5
