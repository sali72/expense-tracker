from collections.abc import AsyncGenerator

import pytest
import requests
import pytest_asyncio
from beanie import init_beanie
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession
import uuid 

from app.api.deps import get_db
from app.core.config import settings
from app.main import app
from app.models import Expense, User
from app.tests.utils import generate_test_access_token


async def get_test_db_client():
    client = AsyncIOMotorClient(settings.MONGODB_LOCAL_URI)
    await init_beanie(
        database=client[settings.TEST_DB_NAME], document_models=[User, Expense]
    )
    return client

async def get_test_db_session() -> AsyncGenerator[AsyncIOMotorClientSession, None, None]:
    client = await get_test_db_client()
    async with await client.start_session() as session:
        print("session", session)
        yield session


@pytest_asyncio.fixture(scope="session")
async def client():
    app.dependency_overrides[get_db] = get_test_db_session
    with TestClient(app) as tc:
        yield tc
    
    client = await get_test_db_client()
    await client.drop_database(settings.TEST_DB_NAME)


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
    user_id = str(uuid.uuid4())
    yield generate_test_access_token(user_id)


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
