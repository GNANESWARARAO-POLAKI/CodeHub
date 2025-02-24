from locust import HttpUser, task, between
from faker import Faker
import random
import os

fake = Faker()
CREDENTIALS_FILE = "user_credentials.txt"
PROFILE_PIC_PATH = "profile.jpg"  # Change this to a valid image file path
TEXT_FILE_PATH = "profile.txt"  # Alternative text file for upload

class StepconeUser(HttpUser):
    wait_time = between(1, 3)  # Simulates a delay between requests

    def get_or_generate_user(self):
        """Fetches existing credentials if available, otherwise generates new ones."""
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, "r") as f:
                data = f.read().strip().split("\n")
                if len(data) >= 2:
                    return data[0], data[1]  # Return stored username and password

        # Generate new credentials
        username = fake.user_name()
        password = fake.password()

        # Store credentials
        with open(CREDENTIALS_FILE, "w") as f:
            f.write(f"{username}\n{password}")

        return username, password

    def get_file(self):
        """Returns a file object if available, otherwise None."""
        if os.path.exists(PROFILE_PIC_PATH):
            return open(PROFILE_PIC_PATH, "rb"), "image/jpeg"
        elif os.path.exists(TEXT_FILE_PATH):
            return open(TEXT_FILE_PATH, "rb"), "text/plain"
        return None, None

    @task
    def signup_test(self):
        """Performs OTP request and signup with file upload."""
        username, password = self.get_or_generate_user()
        email = 'a@gmail.cooss'
        affiliated = random.choice(["1"])  # 0 or 1 as per requirement

        # Request OTP
        otp_payload = {
            "username": username,
            "email": email,
            "affiliated": affiliated,
        }

        otp_response = self.client.post("/stepcone/stepcone_backend/otp.php", json=otp_payload)
        
        if otp_response.status_code == 200:
            otp = random.randint(100000, 999999)  # Simulated OTP for testing
            print(f"OTP Requested for {email}, Using OTP: {otp}")

            # Prepare sign-up data
            signup_payload = {
                "username": username,
                "affiliated": affiliated,
                "jntu": fake.company(),
                "nongmrit_clg": fake.company(),
                "email": email,
                "otp": otp,  # Using a random OTP, replace with actual if needed
                "mobile": fake.phone_number(),
                "year": str(random.randint(1, 4)),
                "branch": "AIDS",
                "password": '11111111',
            }

            # Get file for upload
            file_obj, file_type = self.get_file()
            files = {"profilepic": (os.path.basename(PROFILE_PIC_PATH), file_obj, file_type)} if file_obj else {}

            # Send sign-up request with optional file
            signup_response = self.client.post("/stepcone/stepcone_backend/signUp.php", data=signup_payload, files=files)
            
            if signup_response.status_code == 200:
                print("Signup successful:", signup_response.text)
            else:
                print("Signup failed:", signup_response.status_code, signup_response.text)

            # Close file after sending
            if file_obj:
                file_obj.close()

        else:
            print("OTP request failed:", otp_response.status_code, otp_response.text)
