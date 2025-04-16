from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClientSession as Session

from app.models import Expense, ExpenseCreate, ExpensesPublic, ExpensePublic


async def create_expense(
    *, expense_in: ExpenseCreate, session: Session, user_id: UUID
) -> Expense:
    """
    Create an expense.
    """
    expense = Expense(**expense_in.model_dump(), user_id=user_id)
    await expense.insert(session=session)
    return expense


async def get_expenses(
    *, user_id: UUID, session, skip: int = 0, limit: int = 100
) -> tuple[list[Expense], int]:
    """
    Get paginated expenses for a user.
    Returns a tuple of (expenses_list, total_count)
    """
    query = Expense.find(Expense.user_id == user_id, session=session)

    # Get total count
    total = await query.count()
    
    # Apply pagination
    expenses_list = await query.skip(skip).limit(limit).to_list()

    return expenses_list, total


async def get_expense_for_user(*, expense_id: UUID, user_id: UUID, session) -> Expense:
    """
    Get an expense by id for a user.
    """
    return await Expense.find_one(
        Expense.id == expense_id, Expense.user_id == user_id, session=session
    )


async def update_expense(
    *, expense_id: UUID, user_id: UUID, update_data: dict, session
) -> Expense:
    """
    Update an expense.
    """
    expense = await get_expense_for_user(
        expense_id=expense_id, user_id=user_id, session=session
    )
    if expense:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(expense, key, value)
        await expense.save(session=session)
    return expense


async def delete_expense(*, expense_id: UUID, user_id: UUID, session) -> Expense | None:
    """
    Delete an expense.
    """
    expense = await get_expense_for_user(
        expense_id=expense_id, user_id=user_id, session=session
    )
    if expense:
        await expense.delete(session=session)
        return expense
    return None
