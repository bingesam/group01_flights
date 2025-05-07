import requests
import os
import pandas as pd
from scipy.stats import ttest_ind
from dotenv import load_dotenv
import re

# Token laden
load_dotenv()
TOKEN = os.getenv("TRAVELPAYOUTS_TOKEN")

def fetch_flight_data(origin="ZRH", destination="BCN", currency="CHF"):
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
    
    #print("Status Code:", response.status_code)
    #print("Antworttext:", response.text[:300])  # Nur Vorschau anzeigen
    
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
        duration = item.get("duration")
        found_at = item.get("found_at")
        search_day = extract_search_dayname(found_at)

        if date and price:
            records.append({
                "Reisedatum": date,
                "Preis (CHF)": price,
                "Anzahl Transfers": transfers,
                "Flugdauer (Minuten)": duration,
                "Wochentag der Suche": search_day
            })

    df = pd.DataFrame(records)

    if df.empty:
        print("⚠️ Keine gültigen Flugdaten im DataFrame!")
    else:
        df['Reisedatum'] = pd.to_datetime(df['Reisedatum'])  # Datumsfeld umwandeln

    return df


def analyze_price_distribution(df):
    return df.describe()

def compare_weekday_prices(df):
    df["weekday"] = df["Reisedatum"].dt.day_name()
    weekdays = df.groupby("weekday")["Preis (CHF)"].mean()
    return weekdays

def run_statistical_test(df):
    df["weekday"] = df["Reisedatum"].dt.day_name()
    don = df[df["weekday"] == "Thursday"]["Preis (CHF)"]
    sam = df[df["weekday"] == "Saturday"]["Preis (CHF)"]

    print(f"🔍 Anzahl Flüge - Donnerstag: {len(don)}, Samstag: {len(sam)}")

    if len(don) < 2 or len(sam) < 2:
        print("⚠️ Zu wenig Daten für einen sauberen t-Test.")
        return float('nan'), float('nan')

    t_stat, p_val = ttest_ind(don, sam, equal_var=False)
    return t_stat, p_val

def extract_search_dayname(timestamp):
    """Gibt den Wochentag (Montag, Dienstag, ...) aus einem ISO-Timestamp zurück"""
    match = re.search(r"^(\d{4}-\d{2}-\d{2})", timestamp)
    if match:
        date_str = match.group(1)
        return pd.to_datetime(date_str).day_name()
    return None
