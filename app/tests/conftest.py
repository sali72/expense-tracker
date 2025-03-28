from collections.abc import AsyncGenerator

import pytest
import requests
from beanie import init_beanie
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.main import app
from app.models import Expense, User


@pytest.fixture(scope="session", autouse=True)
async def db() -> AsyncGenerator[AsyncIOMotorClient, None]:
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    test_db_name = settings.MONGODB_DB + "_test"
    await init_beanie(database=client[test_db_name], document_models=[User, Expense])
    yield client
    # Clean up: drop the test database after all tests
    await client.drop_database(test_db_name)
    await client.close()


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as tc:
        yield tc


@pytest.fixture(scope="session")
def real_token():
    """
    Get a token from the real auth service.
    Tests integration with the auth service.
    """
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = "grant_type=password&username=user%40example.com&password=stringst"

    response = requests.post(
        settings.AUTH_SERVICE_TOKEN_URL, headers=headers, data=data
    )

    # Check if request was successful and yield the token
    assert response.status_code == 200, f"Failed to get token: {response.text}"
    yield response.json().get("access_token")


@pytest.fixture(scope="session")
def mock_token():
    """
    Provides a mock JWT token for testing without auth service dependency.
    """
    yield settings.MOCK_TOKEN


@pytest.fixture(scope="session")
def token(request):
    """
    Default token fixture that uses real_token when auth service is available,
    falls back to mock_token otherwise.
    """
    try:
        yield request.getfixturevalue("real_token")
    except Exception:
        yield request.getfixturevalue("mock_token")


@pytest.fixture(scope="session")
def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}
