from app.api.routes import users
from app.api.routes import expenses
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(expenses.router)