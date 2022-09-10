import random

from locust import HttpUser, between, task

jwt_token = ""


class QuickstartUser(HttpUser):
    wait_time = between(1, 4)

    @task
    def get_all_users(self):
        self.client.get(
            f"/api/v1/admin/users?page={random.randint(1, 100)}", headers={"Authorization": f"Bearer {jwt_token}"}
        )

    @task(2)
    def get_random_user(self):
        self.client.get(
            f"/api/v1/admin/users/{random.randint(12684, 112684)}",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
