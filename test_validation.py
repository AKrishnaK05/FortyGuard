import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FORTYGUARD_API_KEY")

if not API_KEY:
    raise RuntimeError("FORTYGUARD_API_KEY is missing. Set it in your .env file.")

headers = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

# Deliberately malformed polygon: coordinates is an empty array.
payload = {
    "polygon_aoi": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": []
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
    "https://api.fortyguard.com/v1/heatmap",
    headers=headers,
    json=payload,
    timeout=60
)

print("HTTP Status:", response.status_code)
print("Response:", response.text)
