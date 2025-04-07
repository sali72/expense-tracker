from beanie import init_beanie
from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

from app.models import Expense, User


async def get_client():
    if settings.DB_MODE == "local":
        client = AsyncIOMotorClient(settings.MONGODB_LOCAL_URI)
    elif settings.DB_MODE == "container":
        client = AsyncIOMotorClient(settings.MONGODB_DOCKER_HOST)
    else:
        raise ValueError("Invalid DB mode")
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME], document_models=[User, Expense]
    )
    return client
