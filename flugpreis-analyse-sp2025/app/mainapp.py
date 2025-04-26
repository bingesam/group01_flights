import requests
import os
from dotenv import load_dotenv

# Token laden
load_dotenv()
TOKEN = os.getenv("TRAVELPAYOUTS_TOKEN")

def fetch_flight_data(origin="FRA", destination="BCN", currency="EUR"):
    url = "https://api.travelpayouts.com/v2/prices/latest"
    
    headers = {
        "X-Access-Token": TOKEN
    }
    
    params = {
        "origin": origin,
        "destination": destination,
        "currency": currency
    }
    
    response = requests.get(url, headers=headers, params=params)
    print("Status Code:", response.status_code)
    print("Antworttext:", response.text)

    print("Status:", response.status_code)
    print("Antwort:", response.text[:300])
    
    if response.status_code != 200:
        print("❗ API Fehler")
        return []
    
    data = response.json()
    return data.get("data", [])
