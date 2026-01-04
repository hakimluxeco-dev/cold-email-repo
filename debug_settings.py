import requests
import json

url = "http://127.0.0.1:8000/settings"

# Simulate the payload sent by Frontend
payload = {
    "smtp_user": "test@example.com",
    "smtp_password": "password123",
    "daily_limit": 50,
    "email_template_body": "Hello"
}

print(f"Testing PUT {url}...")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    response = requests.put(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
