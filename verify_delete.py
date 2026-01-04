import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_delete():
    print("Testing Delete Endpoint...")
    try:
        # First check connection
        r = requests.get(f"{BASE_URL}/")
        print(f"Root check: {r.status_code}")
        
        # Test Delete Payload
        payload = {
            "lead_ids": [1, 2, 3],
            "all": False
        }
        
        print(f"Sending payload: {json.dumps(payload)}")
        r = requests.post(f"{BASE_URL}/leads/delete", json=payload)
        
        print(f"Status Code: {r.status_code}")
        print(f"Response: {r.text}")
        
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    test_delete()
