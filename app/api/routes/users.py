from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClientSession as Session

from app.api.deps import get_db, UserIDDep
from app.crud import users
from app.models import Message, UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/test-auth")
def test(user_id: UserIDDep) -> Any:
    """
    Get current user id.
    """
    return f"Auth test successful for user {user_id}"


@router.post("/", response_model=UserPublic)
async def create_user(user_in: UserCreate, session: Session = Depends(get_db)) -> Any:
    user = await users.get_user(user_id=user_in.id, session=session)
    if user:
        raise HTTPException(status_code=400, detail="user already exists")

    user = await users.create_user(user=user_in, session=session)
    return user


@router.delete("/", response_model=Message)
async def delete_user(id: UUID, session: Session = Depends(get_db)) -> Any:
    user = await users.get_user(user_id=id, session=session)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    await users.delete_user(user_id=id, session=session)
    return Message(message="user deleted")
