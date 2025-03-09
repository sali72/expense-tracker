from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClientSession as Session

from app.api.deps import get_db
from app.crud import users
from app.models import UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic)
async def create_user(user_in: UserCreate, session: Session = Depends(get_db)):
    user = await users.get_user(user_id=user_in.id, session=session)
    if user:
        raise HTTPException(status_code=400, detail="user already exists")
    
    user = await users.create_user(user=user_in, session=session)
    return user
