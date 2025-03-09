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
    

def test_create_duplicate_user(client: TestClient):
    # Generate a valid UUID
    user_id = str(uuid4())
    
    # Create the user first time
    response = client.post(
        "/users/", json={"id": user_id, "expense_ids": []}
    )
    assert response.status_code == 200
    
    # Attempt to create the same user again
    response = client.post(
        "/users/", json={"id": user_id, "expense_ids": []}
    )
    
    # Check that we get a 400 error
    assert response.status_code == 400
    

def test_delete_user(client: TestClient):
    # Generate a valid UUID and create a user first
    user_id = str(uuid4())
    response = client.post(
        "/users/", json={"id": user_id, "expense_ids": []}
    )
    assert response.status_code == 200
    
    # Delete the user
    response = client.delete(f"/users/?user_id={user_id}")
    
    # Check response status and content
    assert response.status_code == 200

    
    # Verify user is actually deleted by trying to delete again
    response = client.delete(f"/users/?user_id={user_id}")
    assert response.status_code == 404


def test_delete_nonexistent_user(client: TestClient):
    # Try to delete a user that doesn't exist
    non_existent_id = str(uuid4())
    response = client.delete(f"/users/?user_id={non_existent_id}")
    
    # Check that we get a 404 error
    assert response.status_code == 404
    assert response.json()["detail"] == "user not found"
