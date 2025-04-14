from fastapi import FastAPI

from app.api.main import api_router

app = FastAPI(
    title="Expense Tracker",
    description="Expense Tracker API"
)

app.include_router(api_router)
