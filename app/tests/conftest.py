from collections.abc import AsyncGenerator

import pytest
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
