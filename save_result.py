import os
import json
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
        "Set it to the completed activity you want to save."
    )

headers = {"api-key": API_KEY}

response = requests.get(
    f"{BASE_URL}/v1/status/{ACTIVITY_ID}",
    headers=headers,
    timeout=30
)

response.raise_for_status()
data = response.json()

if data.get("data", {}).get("status") != "Completed":
    raise RuntimeError("Heatmap task is not completed.")

with open("large_area_result.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print("Result successfully saved to large_area_result.json")
