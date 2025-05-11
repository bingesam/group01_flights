# Import necessary libraries
import requests                  # For API requests (HTTP)
import os                        # For environment variables (e.g., API tokens)
import pandas as pd              # For tabular data processing
from scipy.stats import ttest_ind  # For t-test (statistical analysis)
from dotenv import load_dotenv   # To load environment variables from .env file
import re                        # For regular expressions (Regex)

# Load .env file and get the access token
load_dotenv()
TOKEN = os.getenv("TRAVELPAYOUTS_TOKEN")

# Function to fetch flight data via the Travelpayouts API
def fetch_flight_data(origin="ZRH", destination="BCN", currency="CHF"):
    url = "https://api.travelpayouts.com/v2/prices/latest"  # API endpoint
    headers = {"X-Access-Token": TOKEN}                     # Authentication via header
    params = {
        "origin": origin,
        "destination": destination,
        "currency": currency
    }
    response = requests.get(url, headers=headers, params=params)  # Send request
    if response.status_code != 200:
        print("Error fetching flight data")  # Error handling
        return []
    data = response.json()
    return data.get("data", [])  # Return the "data" list from the API response

# Helper function: extract weekday from timestamp
def extract_search_dayname(timestamp):
    match = re.search(r"^(\d{4}-\d{2}-\d{2})", timestamp)  # Regex for date at the beginning
    if match:
        date_str = match.group(1)
        return pd.to_datetime(date_str).day_name()         # Convert to weekday name
    return None

# Clean API data and convert it into a DataFrame
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

    df = pd.DataFrame(records)  # Create DataFrame

    if not df.empty:
        df['Reisedatum'] = pd.to_datetime(df['Reisedatum'])  # Parse dates correctly

    return df

# Return statistical summary (min, max, mean, quartiles)
def analyze_price_distribution(df):
    return df.describe()

# Group prices by weekday and calculate the mean
def compare_weekday_prices(df):
    df["weekday"] = df["Reisedatum"].dt.day_name()   # Extract weekday
    return df.groupby("weekday")["Preis (CHF)"].mean()  # Calculate average

# Perform a t-test between prices on Thursday and Saturday
def run_statistical_test(df):
    df["weekday"] = df["Reisedatum"].dt.day_name()
    don = df[df["weekday"] == "Thursday"]["Preis (CHF)"]
    sam = df[df["weekday"] == "Saturday"]["Preis (CHF)"]

    if len(don) < 2 or len(sam) < 2:
        return float('nan'), float('nan')  # Not enough data to test

    t_stat, p_val = ttest_ind(don, sam, equal_var=False)
    return t_stat, p_val

# Use Together.ai (Mistral model) to analyze flight price trends
def together_explain_weekday_prices(df):
    # Calculate and sort average prices by weekday
    weekday_avg = df.groupby("weekday")["Preis (CHF)"].mean().sort_values()
    trend_text = "\n".join([f"{tag}: {preis:.2f} CHF" for tag, preis in weekday_avg.items()])

    # Prepare prompt for the language model
    prompt = f"""
        Here are average flight prices per weekday:

    {trend_text}

        Please analyze in 3–4 sentences: When is flying cheapest? Any noticeable trends?
        """

    # Prepare API request to Together.ai
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",  # API key from .env
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",  # Chosen model
        "messages": [
            {"role": "user", "content": prompt}         # Send prompt to model
        ]
    }

    # Send request
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise error if request fails

    # Extract and return the response content
    return response.json()["choices"][0]["message"]["content"]
