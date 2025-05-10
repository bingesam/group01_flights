# Flugpreis-Analyse (Scientific Programming FS2025)

Dieses Projekt untersucht, wie sich Flugpreise abhängig von Wochentag, Reiseziel und Saison verändern. Die Daten werden per Travelpayouts-API abgerufen, in einer SQLite-Datenbank gespeichert und in einer interaktiven Streamlit-App analysiert.

---

## Team

- Delia Troncato
- Samira Binggesser
- Gioia Finocchi

---

## Inhalte

- Web-API-Anbindung (Travelpayouts)
- Datenaufbereitung mit Pandas inkl. Typenumwandlung
- Regex-Nutzung zur Extraktion von Zeitinformationen
- Nutzung von Python-Datenstrukturen (Listen, Dictionaries etc.)
- Kontrollstrukturen: Bedingungen und Schleifen
- Explorative Datenanalyse und Visualisierungen (Matplotlib, Seaborn)
- Statistische Auswertung (t-Test mit p-Wert)
- Speicherung in SQLite-Datenbank inkl. SQL-Query
- Interaktive Streamlit-Web-App zur Darstellung und Analyse
- Analyse mit einem Large Language Model (LLM) via Together.ai
- Analyse im Jupyter Notebook

---

## Projekt starten

### 1. Repository klonen (falls noch nicht geschehen)

### 2. `.env`-Datei erstellen mit deinem API-Zugang

Inhalt der Datei `.env`:

TRAVELPAYOUTS_TOKEN=dein_token_hier
TOGETHER_API_KEY=dein_token_hier

> Wichtig: Diese Datei **nicht ins Repository hochladen** – sie enthält private Zugangsdaten!

### 3. Notwendige Pakete installieren

pip install -r requirements.txt

### 4. Streamlit-Web-App starten

streamlit run app/app_streamlit.py

-> Die App läuft dann lokal im Browser auf http://localhost:8501

---

## Jupyter Notebook

Zur Analyse und Visualisierung kann das begleitende Jupyter Notebook verwendet werden:

### Notebook starten

jupyter lab notebooks/flugpreis_analyse.ipynb

Alternativ in VS Code direkt im Ordner `notebooks/` öffnen.


