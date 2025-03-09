from uuid import UUID
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClientSession as Session

from app.api.deps import get_db
from app.crud import users
from app.models import UserCreate, UserPublic, Message

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic)
async def create_user(user_in: UserCreate, session: Session = Depends(get_db)) -> Any:
    user = await users.get_user(user_id=user_in.id, session=session)
    if user:
        raise HTTPException(status_code=400, detail="user already exists")
    
    user = await users.create_user(user=user_in, session=session)
    return user

@router.delete("/", response_model=Message)
async def delete_user(user_id: UUID, session: Session = Depends(get_db)):
    user = await users.get_user(user_id=user_id, session=session)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    await users.delete_user(user_id=user_id, session=session)
    return Message(message="user deleted")