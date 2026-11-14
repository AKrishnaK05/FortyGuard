
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FORTYGUARD_API_KEY")
BASE_URL = "https://api.fortyguard.com"

activity_id = "7ef65b06-13df-44f7-8d93-eb252060e940"

headers = {"api-key": API_KEY}

response = requests.get(
    f"{BASE_URL}/v1/status/{activity_id}",
    headers=headers,
    timeout=30
)

response.raise_for_status()

data = response.json()

if data.get("data", {}).get("status") != "Completed":
    raise RuntimeError("Heatmap task is not completed.")

with open("large_area_result.json", "w") as file:
    json.dump(data, file, indent=4)

print("Result successfully saved to large_area_result.json")
