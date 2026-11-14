
import os
import time
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FORTYGUARD_API_KEY")
BASE_URL = "https://api.fortyguard.com"

if not API_KEY:
    raise RuntimeError(
        "FORTYGUARD_API_KEY is missing. "
        "Set it in your local .env file."
    )

HEADERS = {
    "api-key": API_KEY,
    "Content-Type": "application/json",
}

payload = {
    "polygon_aoi": {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-119.8180, 36.7275],
                    [-119.8155, 36.7275],
                    [-119.8155, 36.7295],
                    [-119.8180, 36.7295],
                    [-119.8180, 36.7275],
                ]],
            },
        }],
    },
    "date_time": {
        "start_date": "2026-11-14",
        "start_time": "01:00",
        "filter_type": 1,
    },
    "granularity": 100,
}


def main():
    response = requests.post(
        f"{BASE_URL}/v1/heatmap",
        headers=HEADERS,
        json=payload,
        timeout=60,
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
            headers=HEADERS,
            timeout=30,
        )

        print(f"Poll {attempt + 1}: HTTP {status_response.status_code}")

        if status_response.status_code == 404:
            continue

        status_response.raise_for_status()

        status_payload = status_response.json()
        task = status_payload.get("data", {})
        status = task.get("status")

        print("Processing status:", status)

        if status == "Completed":
            output_path = f"heatmap_{activity_id}.json"

            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(status_payload, file, indent=2)

            print("Result saved to:", output_path)
            return

        if status == "Failed":
            raise RuntimeError(
                f"Heatmap processing failed: {status_payload}"
            )

    raise TimeoutError(
        f"Heatmap {activity_id} did not complete within the polling window."
    )


if __name__ == "__main__":
    main()
