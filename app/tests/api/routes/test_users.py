import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4
from app.core.config import settings


@pytest.fixture(scope="function", autouse=True)
async def clean_users_collection(db: AsyncIOMotorClient):
    # Clean up before test
    test_db_name = settings.MONGODB_DB + "_test"
    await db[test_db_name]["users"].delete_many({}) 
    yield


def test_create_user(client: TestClient):
    # Generate a valid UUID
    user_id = str(uuid4())
    
    # Create the user
    response = client.post(
        "/users/", json={"id": user_id, "expense_ids": []}
    )
    
    # Check response status and content
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["expense_ids"] == []
    
