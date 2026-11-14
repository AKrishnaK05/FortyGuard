
import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("FORTYGUARD_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Check your .env file.")

BASE_URL = "https://api.fortyguard.com"

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
                        [-119.8180, 36.7275],
                        [-119.8155, 36.7275],
                        [-119.8155, 36.7295],
                        [-119.8180, 36.7295],
                        [-119.8180, 36.7275]
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

url = f"{BASE_URL}/v1/heatmap"

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=60
)

print("HTTP Status:", response.status_code)
print("Response:", response.text)

activity_id = "2ab168a0-342b-4df6-b272-54df2f22eebe"

status_url = f"{BASE_URL}/v1/status/{activity_id}"

status_response = requests.get(
    status_url,
    headers=headers,
    timeout=30
)

print("Status HTTP:", status_response.status_code)
print("Status response:", status_response.text)