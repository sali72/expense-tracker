from app.core.db import get_client


async def get_db():
    """
    Asynchronous generator dependency that yields a new MongoDB session.
    This pattern ensures that each API call or request operates in its own session.
    """
    client = await get_client()
    async with await client.start_session() as session:
        yield session
