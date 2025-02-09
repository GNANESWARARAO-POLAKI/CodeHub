import requests

# The FastAPI server URL (replace with the correct host and port)
url = "http://172.30.100.208:8000/run/"

# Data to send in the POST request
data = {
    "language": "c",  # Replace with the desired language (e.g., "cpp", "java")
    "code": """
#include <stdio.h>
int main() {
    printf("Hello, World!\\n");
    return 0;
}
"""
}

# Send the POST request
response = requests.post(url, json=data)

# Print the response from the server
if response.status_code == 200:
    print("Output from the server:")
    print(response.json().get("output"))
else:
    print(f"Error {response.status_code}: {response.json().get('detail')}")
