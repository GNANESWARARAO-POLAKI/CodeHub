from locust import HttpUser, task, between
import json

class StepconeUser(HttpUser):
    wait_time = between(1, 3)  # Simulate user behavior

    def on_start(self):
        """Perform login before executing tasks."""
        self.login()

    def login(self):
        """Login request."""
        payload = {"email": "a@gmail.cooss", "password": "11111111"}
        headers = {"Content-Type": "application/json"}

        response = self.client.post("/stepcone/stepcone_backend/login.php", json=payload, headers=headers)
        print(f"✅ Login Response: {response.text}")

        # Extract user details
        response_json = response.json()
        if response_json.get("status") == "success":
            pass
            # print(response_json)
            # self.email = response_json["non_gmruser"]["email"]
            # self.session_cookies = response.cookies  # Store session cookies
        else:
            print(f"❌ Login Failed: {response_json.get('message')}")
            self.stop()

    # @task
    # def register_event(self):
    #     """Simulate event registration request."""
    #     payload = {
    #         "email": self.email,
    #         "teamName": "code",
    #         "teamLead": self.email,
    #         "members": [],
    #         "eventName": "Paper Presentation",
    #         "teamSize": 1,
    #         "amount": 200
    #     }

    #     headers = {
    #         "Content-Type": "application/json",
    #         "Cookie": "; ".join([f"{k}={v}" for k, v in self.session_cookies.items()])
    #     }

    #     response = self.client.post("/stepcone/stepcone_backend/eventregister.php", json=payload, headers=headers)
    #     print(f"📌 Event Registration Response: {response.text}")

