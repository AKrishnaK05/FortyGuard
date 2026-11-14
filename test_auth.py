
import requests

BASE_URL = "https://api.fortyguard.com"

headers = {
    "api-key": "invalid_test_key_12345"
}

activity_id = "7ef65b06-13df-44f7-8d93-eb252060e940"

response = requests.get(
    f"{BASE_URL}/v1/status/{activity_id}",
    headers=headers,
    timeout=30
)

print("HTTP Status:", response.status_code)
print("Response:", response.text)
