from uuid import UUID

from app.models import User, UserCreate


async def create_user(*, user: UserCreate, session) -> User:
    user: User = User(**user.model_dump())
    await user.insert(session=session)
    return user


async def get_user(*, user_id: UUID, session) -> User | None:
    return await User.get(user_id, session=session)


async def update_user(*, user_id: UUID, update_data: dict, session):
    user = await User.get(user_id, session=session)
    if user:
        for key, value in update_data.items():
            setattr(user, key, value)
        await user.save(session=session)
    return user


async def delete_user(*, user_id: UUID, session):
    user = await User.get(user_id, session=session)
    if user:
        await user.delete(session=session)
        return True
    return False
