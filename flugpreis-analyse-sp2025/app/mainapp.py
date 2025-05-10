# Notwendige Bibliotheken importieren
import requests                  # Für API-Anfragen (HTTP)
import os                        # Für Umgebungsvariablen (API-Token etc.)
import pandas as pd              # Für tabellarische Datenverarbeitung
from scipy.stats import ttest_ind  # Für den t-Test (statistische Analyse)
from dotenv import load_dotenv   # Zum Laden von Umgebungsvariablen aus .env-Datei
import re                        # Für reguläre Ausdrücke (Regex)

# .env-Datei laden und Zugriffstoken lesen
load_dotenv()
TOKEN = os.getenv("TRAVELPAYOUTS_TOKEN")

# Funktion zum Abrufen der Flugdaten über die Travelpayouts-API
def fetch_flight_data(origin="ZRH", destination="BCN", currency="CHF"):
    url = "https://api.travelpayouts.com/v2/prices/latest"  # API-Endpunkt
    headers = {"X-Access-Token": TOKEN}                     # Authentifizierung per Header
    params = {
        "origin": origin,
        "destination": destination,
        "currency": currency
    }
    response = requests.get(url, headers=headers, params=params)  # Anfrage senden
    if response.status_code != 200:
        print("Fehler beim Abrufen der Flugdaten")  # Fehlerbehandlung
        return []
    data = response.json()
    return data.get("data", [])  # Gibt die „data“-Liste aus der API-Antwort zurück

# Hilfsfunktion: Wochentag aus Timestamp extrahieren
def extract_search_dayname(timestamp):
    match = re.search(r"^(\d{4}-\d{2}-\d{2})", timestamp)  # Regex für Datumsteil am Anfang
    if match:
        date_str = match.group(1)
        return pd.to_datetime(date_str).day_name()         # Wandle in Wochentag um
    return None

# Daten aus API bereinigen und in DataFrame umwandeln
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

    df = pd.DataFrame(records)  # Erstelle DataFrame

    if not df.empty:
        df['Reisedatum'] = pd.to_datetime(df['Reisedatum'])  # Datum korrekt parsen

    return df

# Gibt statistische Übersicht (Min, Max, Mittelwert, Quartile)
def analyze_price_distribution(df):
    return df.describe()

# Gruppiert Preise nach Wochentag und berechnet den Mittelwert
def compare_weekday_prices(df):
    df["weekday"] = df["Reisedatum"].dt.day_name()   # Wochentag extrahieren
    return df.groupby("weekday")["Preis (CHF)"].mean()  # Durchschnitt berechnen

# Führt t-Test zwischen Preisen am Donnerstag und Samstag durch
def run_statistical_test(df):
    df["weekday"] = df["Reisedatum"].dt.day_name()
    don = df[df["weekday"] == "Thursday"]["Preis (CHF)"]
    sam = df[df["weekday"] == "Saturday"]["Preis (CHF)"]

    if len(don) < 2 or len(sam) < 2:
        return float('nan'), float('nan')  # Kein gültiger Test möglich

    t_stat, p_val = ttest_ind(don, sam, equal_var=False)
    return t_stat, p_val

# Nutzt Together.ai (Mistral-Modell), um Flugpreis-Trends zu analysieren
def together_explain_weekday_prices(df):
    # Durchschnittliche Preise nach Wochentag berechnen und sortieren
    weekday_avg = df.groupby("weekday")["Preis (CHF)"].mean().sort_values()
    trend_text = "\n".join([f"{tag}: {preis:.2f} CHF" for tag, preis in weekday_avg.items()])

    # Prompt für das Sprachmodell vorbereiten
    prompt = f"""
        Hier sind durchschnittliche Flugpreise pro Wochentag:

    {trend_text}

        Analysiere bitte in 3–4 Sätzen: Wann ist Fliegen am günstigsten? Gibt es Auffälligkeiten?
        """

    # API-Aufruf an Together.ai vorbereiten
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",  # API-Key aus .env-Datei
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",  # Verwendetes Modell
        "messages": [
            {"role": "user", "content": prompt}         # Prompt an das Modell
        ]
    }

    # Anfrage absenden
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Fehler werfen, wenn die Antwort nicht 200 ist

    # Antworttext extrahieren und zurückgeben
    return response.json()["choices"][0]["message"]["content"]
