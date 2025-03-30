from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClientSession as Session

from app.models import Expense, ExpenseCreate


async def create_expense(
    *, expense_in: ExpenseCreate, session: Session, user_id: UUID
) -> Expense:
    """
    Create an expense.
    """
    expense = Expense(**expense_in.model_dump(), user_id=user_id)
    await expense.insert(session=session)
    return expense


async def get_expenses(*, user_id: UUID, session) -> list[Expense]:
    """
    Get all expenses for a user.
    """
    return await Expense.find(Expense.user_id == user_id, session=session).to_list()


async def get_expense_for_user(*, expense_id: UUID, user_id: UUID, session) -> Expense:
    """
    Get an expense by id for a user.
    """
    return await Expense.find_one(
        Expense.id == expense_id, Expense.user_id == user_id, session=session
    )


async def update_expense(*, expense_id: UUID, update_data: dict, session) -> Expense:
    """
    Update an expense.
    """
    expense = await Expense.get(expense_id, session=session)
    if expense:
        for key, value in update_data.items():
            setattr(expense, key, value)
        await expense.save(session=session)
    return expense


async def delete_expense(*, expense_id: UUID, session) -> bool:
    """
    Delete an expense.
    """
    expense = await Expense.get(expense_id, session=session)
    if expense:
        await expense.delete(session=session)
        return True
    return False
