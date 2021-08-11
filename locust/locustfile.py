import json
import random

from locust import HttpUser, between, task


class QuickstartUser(HttpUser):
    wait_time = between(1, 4)

    @task
    def get_all_users(self):
        self.client.get("/api/v1/admin/user")

    @task(2)
    def create_user(self):
        user_id = random.randint(1, 100000)
        load = {
            "username": f"example{user_id}",
            "email": f"user{user_id}@example.com",
            "is_active": "true",
            "password": "string",
        }

        myheaders = {"Content-Type": "application/json", "Accept": "application/json"}
        self.client.post("/api/v1/user/", data=json.dumps(load), headers=myheaders)
