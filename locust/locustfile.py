import json
import random

from locust import HttpUser, between, task

jwt_token = "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbnRvaW5lIiwiZXhwIjoxNjU5ODk1ODgyfQ.uY6A87_8A6KN_DZcE7T-qmSCRDW4-7IUVwnEdRDQooRLDyOuEx7LCjqpWqcjz1xe"


class QuickstartUser(HttpUser):
    wait_time = between(1, 4)

    @task
    def get_all_users(self):
        self.client.get(
            "/api/v1/admin/users", headers={"Authorization": f"Bearer {jwt_token}"}
        )

    @task(2)
    def get_random_user(self):
        self.client.get(
            f"/api/v1/admin/users/{random.randint(68, 200)}", headers={"Authorization": f"Bearer {jwt_token}"}
        )
"""
    @task(2)
    def create_user(self):
        for i in range(1, 200):
            load = {
                "username": f"example{i}",
                "email": f"user{i}@example.com",
                "is_active": "true",
                "password": "string",
            }

            myheaders = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            self.client.post("/api/v1/auth/signup", data=json.dumps(load), headers=myheaders)
"""