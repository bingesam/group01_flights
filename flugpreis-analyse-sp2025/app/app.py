import requests
import pandas as pd
import re
from scipy.stats import ttest_ind
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TRAVELPAYOUTS_TOKEN")

def fetch_flight_data(origin="FRA", destination="BCN", currency="EUR"):
    #url = "https://api.travelpayouts.com/v1/prices/calendar"
    url = "https://aviasales.tp.st/yqxWZ4Yn
    params = {
        "origin": origin,
        "destination": destination,
        "currency": currency,
        "token": TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["data"]

def prepare_dataframe(api_data):
    # Struktur in pandas bringen
    records = []
    for date, info in api_data.items():
        price = info.get("price")
        if price:
            records.append({
                "date": date,
                "price": price,
                "transfers": info.get("transfers", 0)
            })
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
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
