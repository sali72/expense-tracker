from collections.abc import AsyncGenerator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from motor.motor_asyncio import AsyncIOMotorClientSession
from pydantic import ValidationError
import logging
from app.core.config import settings
from app.core.db import get_client

logger = logging.getLogger(__name__)
async def get_db() -> AsyncGenerator[AsyncIOMotorClientSession, None, None]:
    """
    Asynchronous generator dependency that yields a new MongoDB session.
    This pattern ensures that each API call or request operates in its own session.
    """
    client = await get_client()
    async with await client.start_session() as session:
        yield session


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=settings.AUTH_SERVICE_TOKEN_URL)

SessionDep = Annotated[AsyncIOMotorClientSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_token(token: TokenDep) -> str:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return payload["sub"]

UserIDDep = Annotated[str, Depends(get_token)]
