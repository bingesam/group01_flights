# Notwendige Bibliotheken importieren
import sqlite3
import pandas as pd

# Funktion zum Speichern eines DataFrames in die SQLite-Datenbank
def save_to_database(df, db_path="/workspaces/group01_flights/flugpreis-analyse-sp2025/data/fluege.db"):
    conn = sqlite3.connect(db_path)  # Verbindung zur Datenbank herstellen
    df.to_sql("flugpreise", conn, if_exists="replace", index=False)  # Tabelle 'flugpreise' speichern (alte Version wird ersetzt)
    conn.close()  # Verbindung wieder schließen

# Funktion zum Laden aller Flugdaten aus der Datenbank
def load_from_database(db_path="/workspaces/group01_flights/flugpreis-analyse-sp2025/data/fluege.db"):
    conn = sqlite3.connect(db_path)  # Verbindung herstellen
    try:
        df = pd.read_sql("SELECT * FROM flugpreise", conn)  # SQL-Abfrage zum Laden aller Daten
    except Exception as e:
        print("Fehler beim Laden aus der DB:", e)  # Fehlerbehandlung, z. B. falls Tabelle nicht existiert
        df = pd.DataFrame()  # Leeren DataFrame zurückgeben, um Absturz zu vermeiden
    conn.close()
    return df  # Ergebnis zurückgeben

# Funktion zum Abfragen des durchschnittlichen Flugpreises pro Wochentag (direkt per SQL)
def query_average_price_per_weekday(db_path="/workspaces/group01_flights/flugpreis-analyse-sp2025/data/fluege.db"):
    conn = sqlite3.connect(db_path)  # Verbindung zur Datenbank
    query = """
    SELECT strftime('%w', Reisedatum) AS WochentagNum,  -- Extrahiere numerischen Wochentag (0=Sonntag, ..., 6=Samstag)
           CASE strftime('%w', Reisedatum)              -- Wandelt Wochentagsnummer in Klartext um
               WHEN '0' THEN 'Sunday'
               WHEN '1' THEN 'Monday'
               WHEN '2' THEN 'Tuesday'
               WHEN '3' THEN 'Wednesday'
               WHEN '4' THEN 'Thursday'
               WHEN '5' THEN 'Friday'
               WHEN '6' THEN 'Saturday'
           END AS Wochentag,
           AVG("Preis (CHF)") AS Durchschnittspreis     -- Berechne Durchschnittspreis pro Tag
    FROM flugpreise
    GROUP BY WochentagNum                                -- Gruppiere nach numerischem Wochentag (für richtige Reihenfolge)
    ORDER BY WochentagNum                                -- Sortiere nach Tagesreihenfolge (nicht alphabetisch)
    """
    df = pd.read_sql(query, conn)  # SQL-Abfrage ausführen und Ergebnis als DataFrame laden
    conn.close()  # Verbindung schliessen
    return df     # Ergebnis zurückgeben
