from typing import Any

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClientSession as Session

from app.api.deps import UserIDDep, get_db
from app.crud import expenses
from app.models import ExpenseCreate, ExpensePublic

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=ExpensePublic)
async def create_expense(
    expense_in: ExpenseCreate, user_id: UserIDDep, session: Session = Depends(get_db)
) -> Any:
    """
    Create an expense.
    """
    expense = await expenses.create_expense(expense_in=expense_in, session=session, user_id=user_id)
    return expense
