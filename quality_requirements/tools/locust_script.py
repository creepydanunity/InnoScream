from locust import HttpUser, task, between, events
import time
import random
import requests  # Import this for catching HTTPError
from fastapi.exceptions import HTTPException

class TelegramBotUser(HttpUser):
    wait_time = between(0.01, 0.01)

    def on_start(self):
        """Setup any initial configurations (e.g., user ID)"""
        self.user_id = str(random.randint(100000, 999999))

    @task(3)
    def create_scream(self):
        """Simulate creating a scream for a user"""
        start_time = time.time()

        data = {
            "user_id": self.user_id,
            "content": "This is a scream!"
        }

        response = self.client.post("/scream", json=data)

        response_time = time.time() - start_time
        self.record_performance("/scream", response_time)

    @task(4)
    def react_to_scream(self):
        """Simulate reacting to a scream"""
        scream_id = random.randint(1, 10)
        emoji = random.choice(["😡", "😂", "❤️", "❌"])

        start_time = time.time()

        data = {
            "user_id": self.user_id,
            "scream_id": scream_id,
            "emoji": emoji
        }

        with self.client.post("/react", json=data, catch_response=True) as response: 
            if response.status_code == 409:
                print(f"Already reacted to scream {scream_id}.")
                response.success()
            elif response.status_code == 404:
                print(f"Scream {scream_id} was deleted.")
                response.success()
            
            self.record_performance("/react", time.time() - start_time)

    @task(3)
    def get_top_screams(self):
        """Simulate getting top screams"""
        n = random.randint(1, 5)
        start_time = time.time()

        response = self.client.get(f"/top?n={n}")

        response_time = time.time() - start_time
        self.record_performance("/top", response_time)

    @task(2)
    def get_user_stats(self):
        """Simulate getting user stats"""
        start_time = time.time()

        response = self.client.get(f"/stats/{self.user_id}")

        response_time = time.time() - start_time
        self.record_performance("/stats", response_time)

    @task(3)
    def get_weekly_stress(self):
        """Simulate fetching weekly stress stats"""
        start_time = time.time()

        response = self.client.get("/stress")

        response_time = time.time() - start_time
        self.record_performance("/stress", response_time)

    @task(2)
    def delete_scream(self):
        """Simulate deleting a scream as an admin"""
        scream_id = random.randint(1, 10)
        start_time = time.time()

        data = {
            "scream_id": scream_id,
            "user_id": "884905627"
        }

        with self.client.post("/delete", json=data, catch_response=True) as response: 
            response_time = time.time() - start_time

            if response.status_code == 404:
                print(f"Scream with ID {scream_id} not found (already deleted)")
                response.success()

            self.record_performance("/delete", response_time)

    def record_performance(self, endpoint, response_time):
        """Helper function to log the performance and fire Locust event"""
        print(f"Endpoint {endpoint} - Response Time: {response_time:.4f} seconds")
        
        events.request.fire(
            request_type="POST" if 'post' in endpoint.lower() else "GET",
            name=endpoint,
            response_time=int(response_time * 1000),  # Convert to milliseconds
            response_length=0  # Placeholder for response length
        )
