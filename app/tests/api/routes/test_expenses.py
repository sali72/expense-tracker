import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


@pytest.fixture(scope="function", autouse=True)
async def clean_expenses_collection(db: AsyncIOMotorClient):
    test_db_name = settings.TEST_DB_NAME
    await db[test_db_name]["expenses"].delete_many({})
    yield


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
    
