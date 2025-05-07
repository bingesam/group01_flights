import sqlite3
import pandas as pd

def save_to_database(df, db_path="/workspaces/group01_flights/flugpreis-analyse-sp2025/data/fluege.db"):
    conn = sqlite3.connect(db_path)
    df.to_sql("flugpreise", conn, if_exists="replace", index=False)
    conn.close()

def load_from_database(db_path="/workspaces/group01_flights/flugpreis-analyse-sp2025/data/fluege.db"):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM flugpreise", conn)
    except Exception as e:
        print("Fehler beim Laden aus der DB:", e)
        df = pd.DataFrame()  # leeres df zurückgeben
    conn.close()
    return df

def query_average_price_per_weekday(db_path="/workspaces/group01_flights/flugpreis-analyse-sp2025/data/fluege.db"):
    conn = sqlite3.connect(db_path)
    query = """
    SELECT strftime('%w', Reisedatum) AS WochentagNum,
           CASE strftime('%w', Reisedatum)
               WHEN '0' THEN 'Sunday'
               WHEN '1' THEN 'Monday'
               WHEN '2' THEN 'Tuesday'
               WHEN '3' THEN 'Wednesday'
               WHEN '4' THEN 'Thursday'
               WHEN '5' THEN 'Friday'
               WHEN '6' THEN 'Saturday'
           END AS Wochentag,
           AVG("Preis (CHF)") AS Durchschnittspreis
    FROM flugpreise
    GROUP BY WochentagNum
    ORDER BY WochentagNum
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
