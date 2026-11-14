
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FORTYGUARD_API_KEY")
BASE_URL = "https://api.fortyguard.com"

if not API_KEY:
    raise ValueError("API key not found. Check your .env file.")

headers = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "polygon_aoi": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-119.823, 36.724],
                        [-119.811, 36.724],
                        [-119.811, 36.734],
                        [-119.823, 36.734],
                        [-119.823, 36.724]
                    ]]
                }
            }
        ]
    },
    "date_time": {
        "start_date": "2026-11-14",
        "start_time": "01:00",
        "filter_type": 1
    },
    "granularity": 100
}

response = requests.post(
    f"{BASE_URL}/v1/heatmap",
    headers=headers,
    json=payload,
    timeout=60
)

print("Submission HTTP:", response.status_code)

response.raise_for_status()
submission = response.json()

if submission.get("error"):
    raise RuntimeError(f"Submission failed: {submission}")

activity_id = submission["data"]["activity_id"]
print("Activity ID:", activity_id)

status_url = f"{BASE_URL}/v1/status/{activity_id}"

for attempt in range(12):
    time.sleep(5)

    status_response = requests.get(
        status_url,
        headers=headers,
        timeout=30
    )

    print(f"Polling attempt {attempt + 1}: HTTP {status_response.status_code}")

    if status_response.status_code == 404:
        continue

    status_response.raise_for_status()
    result_data = status_response.json()

    task = result_data.get("data", {})
    status = task.get("status")

    print("Processing status:", status)

    if status == "Completed":
        result = task.get("result", {})
        features = result.get("map_data", {}).get("features", [])
        stats = result.get("stats_data", {}).get("temperature_stats", {})

        print("\n--- HEATMAP RESULTS ---")
        print("Activity ID:", task.get("activity_id"))
        print("Number of tiles:", len(features))
        print("Temperature statistics:", stats)

        temperatures = [
            feature.get("properties", {}).get("average_temperature")
            for feature in features
            if feature.get("properties", {}).get("average_temperature") is not None
        ]

        if temperatures:
            print("Tile temperature range:",
                  min(temperatures), "to", max(temperatures))

        break

    elif status == "Failed":
        print("Task failed:", result_data)
        break

else:
    print("Task did not complete within the polling window.")
