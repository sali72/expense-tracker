from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClientSession as Session

from app.api.deps import UserIDDep, get_db
from app.crud import expenses
from app.models import ExpenseCreate, ExpensePublic, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=ExpensePublic)
async def create_expense(
    expense_in: ExpenseCreate, user_id: UserIDDep, session: Session = Depends(get_db)
) -> Any:
    """
    Create an expense.
    """
    expense = await expenses.create_expense(
        expense_in=expense_in, session=session, user_id=user_id
    )
    return expense


@router.get("/", response_model=List[ExpensePublic])
async def get_expenses(user_id: UserIDDep, session: Session = Depends(get_db)) -> Any:
    """
    Get all expenses for a user.
    """
    return await expenses.get_expenses(user_id=user_id, session=session)


@router.get("/{expense_id}", response_model=ExpensePublic)
async def get_expense(
    expense_id: UUID, user_id: UserIDDep, session: Session = Depends(get_db)
) -> Any:
    """
    Get an expense by id.
    """
    expense = await expenses.get_expense_for_user(
        expense_id=expense_id, user_id=user_id, session=session
    )
    if not expense:
        raise HTTPException(status_code=404, detail="expense not found")
    return expense


@router.patch("/{expense_id}", response_model=ExpensePublic)
async def update_expense(
    expense_id: UUID,
    expense_in: ExpenseUpdate,
    user_id: UserIDDep,
    session: Session = Depends(get_db),
) -> Any:
    """
    Update an expense.
    """
    expense = await expenses.update_expense(
        expense_id=expense_id,
        user_id=user_id,
        update_data=expense_in,
        session=session,
    )
    if not expense:
        raise HTTPException(status_code=404, detail="expense not found")
    return expense
