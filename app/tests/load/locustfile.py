import uuid
import jwt
from app.core.config import settings
from datetime import datetime, timedelta

from locust import HttpUser, between, task


class NormalUser(HttpUser):
    wait_time = between(1, 3)  # Wait between 1-3 seconds between tasks

    def on_start(self):
        # Generate a unique user ID for this test user
        user_id = str(uuid.uuid4())
        self.client.post(
            settings.EXPENSE_TRACKER_URL + "/users",
            json={"id": user_id},
        )
        
        self.access_token = self._generate_access_token(user_id)
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        
    def _generate_access_token(self, user_id: str) -> str:
        payload = {
            "exp": datetime.now() + timedelta(days=30),
            "sub": user_id
        }
        return jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        


    @task(3)
    def create_expense(self):
        expense_data = {
            "amount": 29.99,
            "tag": "food",
            "description": f"Test expense {uuid.uuid4()}",
        }

        self.client.post(
            settings.EXPENSE_TRACKER_URL + "/expenses",
            json=expense_data,
            headers=self.headers,
        )

    @task(5)
    def list_expenses(self):
        self.client.get(
            settings.EXPENSE_TRACKER_URL + "/expenses", headers=self.headers
        )

    @task(1)
    def get_expense(self):
        # First get all expenses to find one to retrieve
        response = self.client.get(
            settings.EXPENSE_TRACKER_URL + "/expenses", headers=self.headers
        )

        if response.status_code == 200:
            expenses = response.json()
            if expenses:
                expense_id = expenses[0]["id"]
                self.client.get(
                    settings.EXPENSE_TRACKER_URL + f"/expenses/{expense_id}",
                    headers=self.headers,
                    name="/expenses/{id}"
                )

    @task(1)
    def update_expense(self):
        # First get all expenses to find one to update
        response = self.client.get(
            settings.EXPENSE_TRACKER_URL + "/expenses", headers=self.headers
        )

        if response.status_code == 200:
            expenses = response.json()
            if expenses:
                expense_id = expenses[0]["id"]
                update_data = {
                    "amount": 39.99,
                    "description": f"Updated expense {uuid.uuid4()}",
                }

                self.client.patch(
                    settings.EXPENSE_TRACKER_URL + f"/expenses/{expense_id}",
                    json=update_data,
                    headers=self.headers,
                    name="/expenses/{id}"
                )

    @task(1)
    def delete_expense(self):
        response = self.client.get(
            settings.EXPENSE_TRACKER_URL + "/expenses", headers=self.headers
        )

        if response.status_code == 200:
            expenses = response.json()
            if expenses:
                expense_id = expenses[0]["id"]
                self.client.delete(
                    settings.EXPENSE_TRACKER_URL + f"/expenses/{expense_id}",
                    headers=self.headers,
                    name="/expenses/{id}"
                )

