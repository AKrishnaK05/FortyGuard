import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FORTYGUARD_API_KEY")
ACTIVITY_ID = os.getenv("FORTYGUARD_ACTIVITY_ID")
BASE_URL = "https://api.fortyguard.com"

if not API_KEY:
    raise RuntimeError("FORTYGUARD_API_KEY is missing. Set it in your .env file.")

if not ACTIVITY_ID:
    raise RuntimeError(
        "FORTYGUARD_ACTIVITY_ID is missing. "
        "Set it to the activity ID you want to inspect."
    )

headers = {"api-key": API_KEY}
url = f"{BASE_URL}/v1/status/{ACTIVITY_ID}"

response = requests.get(url, headers=headers, timeout=30)

print("HTTP Status:", response.status_code)
print("Response:", response.text)
