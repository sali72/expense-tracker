import uuid
from app.core.config import settings
from app.tests.utils import generate_test_access_token

from locust import HttpUser, between, task
import logging


class NormalUser(HttpUser):
    wait_time = between(1, 3)  # Wait between 1-3 seconds between tasks

    def on_start(self):
        # Generate a unique user ID for this test user
        self.user_id = str(uuid.uuid4())
        self.client.post(
            settings.EXPENSE_TRACKER_URL + "/users",
            json={"id": self.user_id},
        )

        self.access_token = generate_test_access_token(self.user_id)
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

        # Initialize a list to store expense IDs created by this user
        self.expense_ids = []

        # Create an initial expense to work with
        self._create_initial_expense()


    def _create_initial_expense(self):
        """Create an initial expense and store its ID"""
        expense_data = {
            "amount": 29.99,
            "tag": "food",
            "description": f"Initial expense {uuid.uuid4()}",
        }

        response = self.client.post(
            settings.EXPENSE_TRACKER_URL + "/expenses",
            json=expense_data,
            headers=self.headers,
        )

        if response.status_code == 200:
            expense_id = response.json()["id"]
            self.expense_ids.append(expense_id)
            logging.info(
                f"Created initial expense with ID: {expense_id} for user: {self.user_id}"
            )

    @task(3)
    def create_expense(self):
        expense_data = {
            "amount": 29.99,
            "tag": "food",
            "description": f"Test expense {uuid.uuid4()}",
        }

        response = self.client.post(
            settings.EXPENSE_TRACKER_URL + "/expenses",
            json=expense_data,
            headers=self.headers,
        )

        if response.status_code == 200:
            expense_id = response.json()["id"]
            self.expense_ids.append(expense_id)
            # Limit the number of stored IDs to prevent memory issues
            if len(self.expense_ids) > 10:
                self.expense_ids = self.expense_ids[-10:]

    @task(5)
    def list_expenses(self):
        self.client.get(
            settings.EXPENSE_TRACKER_URL + "/expenses", headers=self.headers
        )

    @task(1)
    def get_expense(self):
        if not self.expense_ids:
            return

        # Use one of our own expense IDs
        expense_id = self.expense_ids[0]
        self.client.get(
            settings.EXPENSE_TRACKER_URL + f"/expenses/{expense_id}",
            headers=self.headers,
            name="/expenses/{id}",
        )

    @task(1)
    def update_expense(self):
        if not self.expense_ids:
            return

        # Use one of our own expense IDs
        expense_id = self.expense_ids[0]
        update_data = {
            "amount": 39.99,
            "description": f"Updated expense {uuid.uuid4()}",
        }

        self.client.patch(
            settings.EXPENSE_TRACKER_URL + f"/expenses/{expense_id}",
            json=update_data,
            headers=self.headers,
            name="/expenses/{id}",
        )

    @task(1)
    def delete_expense(self):
        if not self.expense_ids:
            return

        # Use one of our own expense IDs and remove it from the list
        expense_id = self.expense_ids.pop()
        self.client.delete(
            settings.EXPENSE_TRACKER_URL + f"/expenses/{expense_id}",
            headers=self.headers,
            name="/expenses/{id}",
        )

        # Create a new expense if we're running low
        if not self.expense_ids:
            self._create_initial_expense()
