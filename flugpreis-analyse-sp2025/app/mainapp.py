import requests
import os
import pandas as pd
from scipy.stats import ttest_ind
from dotenv import load_dotenv
import re
import requests

load_dotenv()
TOKEN = os.getenv("TRAVELPAYOUTS_TOKEN")

def fetch_flight_data(origin="ZRH", destination="BCN", currency="CHF"):
    url = "https://api.travelpayouts.com/v2/prices/latest"
    headers = {"X-Access-Token": TOKEN}
    params = {
        "origin": origin,
        "destination": destination,
        "currency": currency
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("❗ Fehler beim Abrufen der Flugdaten")
        return []
    data = response.json()
    return data.get("data", [])

def extract_search_dayname(timestamp):
    match = re.search(r"^(\d{4}-\d{2}-\d{2})", timestamp)
    if match:
        date_str = match.group(1)
        return pd.to_datetime(date_str).day_name()
    return None

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

    if not df.empty:
        df['Reisedatum'] = pd.to_datetime(df['Reisedatum'])

    return df

def analyze_price_distribution(df):
    return df.describe()

def compare_weekday_prices(df):
    df["weekday"] = df["Reisedatum"].dt.day_name()
    return df.groupby("weekday")["Preis (CHF)"].mean()

def run_statistical_test(df):
    df["weekday"] = df["Reisedatum"].dt.day_name()
    don = df[df["weekday"] == "Thursday"]["Preis (CHF)"]
    sam = df[df["weekday"] == "Saturday"]["Preis (CHF)"]

    if len(don) < 2 or len(sam) < 2:
        return float('nan'), float('nan')

    t_stat, p_val = ttest_ind(don, sam, equal_var=False)
    return t_stat, p_val

def together_explain_weekday_prices(df):
    weekday_avg = df.groupby("weekday")["Preis (CHF)"].mean().sort_values()
    trend_text = "\n".join([f"{tag}: {preis:.2f} CHF" for tag, preis in weekday_avg.items()])

    prompt = f"""
Hier sind durchschnittliche Flugpreise pro Wochentag:

{trend_text}

Analysiere bitte in 3–4 Sätzen: Wann ist Fliegen am günstigsten? Gibt es Auffälligkeiten?
"""

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
