from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # Define the base host of your site (adjust if not running locally)
    host = "http://127.0.0.1:8000"  # Replace with your actual host if different
    wait_time = between(1, 2)  # Wait time between tasks (1 to 5 seconds)

    @task
    def codelife_details(self):
        # Test the "codelife details" page 
        self.client.get("/login/")

    @task
    def contests_page(self):
        # Test the "contests" page
        self.client.get("/")

# from locust import HttpUser, task, between
# from faker import Faker
# import random
# import re

# fake = Faker()

# class WebsiteUser(HttpUser):
#     host = "http://127.0.0.1:8000"  # Adjust to your Django server
#     wait_time = between(1, 5)  # Simulate real user wait times

#     # Registration Task
#     @task(1)
#     def test_register_post(self):
#         # Generate random unique user data for each request
#         username = fake.user_name()
#         email = fake.email()
#         password = fake.password()
#         first_name = fake.first_name()
#         last_name = fake.last_name()
#         phone = fake.phone_number()
#         jntuno = fake.uuid4()
#         branch = random.choice(['CSE', 'ECE', 'ME', 'EEE'])
#         college = fake.company()

#         data = {
#             "username": username,
#             "first_name": first_name,
#             "last_name": last_name,
#             "email": email,
#             "phone": phone,
#             "jntuno": jntuno,
#             "branch": branch,
#             "college": college,
#             "password": password,
#         }

#         response = self.client.post("/register", data=data)
#         print(f"Register response: {response.status_code}, {response.text}")  # Log response

#     # Login Task with CSRF Token Handling
#     @task(2)
#     def test_login_post(self):
#         # Fetch the CSRF token from the login page first
#         login_page_response = self.client.get("/login/")
#         csrf_token = self.extract_csrf_token(login_page_response.text)

#         # Prepare login data
#         username = fake.user_name()  # Use the same username as registered
#         password = "testpassword"  # Use the same password as generated in registration

#         # Send the login POST request with CSRF token included
#         response = self.client.post("/login/", data={
#             "username": username,
#             "password": password,
#             "csrfmiddlewaretoken": csrf_token,
#         }, headers={"Referer": "/login/"})  # Add a referer header

#         print(f"Login response: {response.status_code}, {response.text}")  # Log response

#     def extract_csrf_token(self, html):
#         """Extract the CSRF token from the HTML response"""
#         csrf_token_match = re.search(r'csrfmiddlewaretoken" value="([a-f0-9]{32})"', html)
#         return csrf_token_match.group(1) if csrf_token_match else None

#     # Register for Contest Task
#     @task(3)
#     def test_register_for_contest(self):
#         contest_id = 1  # Contest ID to register for
#         response = self.client.post(f"/codelife/{contest_id}/register", data={})
#         print(f"Contest registration response: {response.status_code}, {response.text}")  # Log response
