from beanie import init_beanie
from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from functools import cache
from app.models import Expense, User

# Non-async function for creating the client
@cache
def create_motor_client():
    """Create and cache a MongoDB client - one per process."""
    if settings.DB_MODE == "local":
        return AsyncIOMotorClient(settings.MONGODB_LOCAL_URI)
    elif settings.DB_MODE == "container":
        return AsyncIOMotorClient(settings.MONGODB_DOCKER_HOST)
    else:
        raise ValueError("Invalid DB mode")

# Async function for initialization
async def get_client():
    """Get the client and ensure Beanie is initialized."""
    client = create_motor_client()
    # Only initialize Beanie once per client
    if not hasattr(client, '_beanie_initialized'):
        await init_beanie(
            database=client[settings.MONGODB_DB_NAME], 
            document_models=[User, Expense]
        )
        client._beanie_initialized = True
    return client
