from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID, uuid4

from beanie import Document
from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    id: UUID = Field(..., description="User ID")
    expense_ids: List[UUID] = Field(
        default_factory=list, description="List of user's expense IDs"
    )


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    pass


class User(Document, UserBase):
    id: UUID = Field(..., description="User ID")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "expense_ids": [
                    "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                ],
            }
        }
    )

    class Settings:
        name = "users"
        use_state_management = True
        use_uuid_representation = True



class ExpenseTag(str, Enum):
    FOOD = "food"
    TRANSPORTATION = "transportation"
    TRAVEL = "travel"
    ENTERTAINMENT = "entertainment"
    GROCERIES = "groceries"
    LEISURE = "leisure"
    ELECTRONICS = "electronics"
    UTILITIES = "utilities"
    CLOTHING = "clothing"
    HEALTH = "health"
    OTHER = "other"


class ExpenseBase(BaseModel):
    amount: float = Field(..., description="Expense amount")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Expense timestamp"
    )
    tag: ExpenseTag = Field(
        default=ExpenseTag.OTHER, description="Tag for expense categorization"
    )
    description: str | None = Field(
        default=None, description="Optional expense description"
    )


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    amount: float | None = None
    tag: ExpenseTag | None = None


class ExpensePublic(ExpenseBase):
    id: UUID = Field(default_factory=uuid4, description="Expense ID")


class ExpensesPublic(BaseModel):
    data: list[ExpensePublic]
    count: int


class Expense(Document, ExpenseBase):
    id: UUID = Field(default_factory=uuid4, description="Expense ID")
    user_id: UUID = Field(..., description="User ID")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": 29.99,
                "tag": "food",
                "description": "Lunch at restaurant",
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            }
        }
    )

    class Settings:
        name = "expenses"
        use_state_management = True
        use_uuid_representation = True

class Message(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"