from beanie import init_beanie
from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

from app.models import Expense, User


async def get_client():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    await init_beanie(
        database=client[settings.MONGODB_DB], document_models=[User, Expense]
    )
    return client
