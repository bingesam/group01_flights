import requests
import os
import pandas as pd
from scipy.stats import ttest_ind
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
    print("Antworttext:", response.text[:300])  # Nur Vorschau anzeigen
    
    if response.status_code != 200:
        print("❗ Fehler beim Abrufen der Flugdaten")
        return []
    
    data = response.json()
    return data.get("data", [])


def prepare_dataframe(api_data):
    records = []
    for item in api_data:
        date = item.get("depart_date")
        price = item.get("value")
        transfers = item.get("number_of_changes", 0)
        
        if date and price:
            records.append({
                "date": date,
                "price": price,
                "transfers": transfers
            })
    
    df = pd.DataFrame(records)
    
    if df.empty:
        print("⚠️ Keine gültigen Flugdaten im DataFrame!")
    else:
        df['date'] = pd.to_datetime(df['date'])  # Datumsfeld umwandeln
    
    return df

def analyze_price_distribution(df):
    return df.describe()

def compare_weekday_prices(df):
    df["weekday"] = df["date"].dt.day_name()
    weekdays = df.groupby("weekday")["price"].mean()
    return weekdays

def run_statistical_test(df):
    df["weekday"] = df["date"].dt.day_name()
    mon = df[df["weekday"] == "Monday"]["price"]
    fri = df[df["weekday"] == "Friday"]["price"]
    t_stat, p_val = ttest_ind(mon, fri, equal_var=False)
    return t_stat, p_val
