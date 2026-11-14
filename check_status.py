import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FORTYGUARD_API_KEY")
BASE_URL = "https://api.fortyguard.com"

activity_id = "6999e197-e95e-4f95-8b4c-b9d0e7f792fb"

headers = {"api-key": API_KEY}

url = f"{BASE_URL}/v1/status/{activity_id}"

response = requests.get(url, headers=headers, timeout=30)

print("HTTP Status:", response.status_code)
print("Response:", response.text)