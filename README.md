# Flugpreis-Analyse (SP 2025)

Dieses Projekt untersucht, wie sich Flugpreise abhängig von Wochentag, Reiseziel und Saison verändern. Die Daten werden per Travelpayouts-API abgerufen, in einer SQLite-Datenbank gespeichert und in einer interaktiven Streamlit-App analysiert.

---

## Team

- Delia Troncato
- Samira Binggesser
- Gioia Finocchi

---

## Inhalte

- Web-API-Anbindung (Travelpayouts)
- Datenaufbereitung mit Pandas
- Regex-Nutzung zur Zeitanalyse
- Explorative Datenanalyse und Visualisierungen
- Statistische Auswertung (t-Test mit p-Wert)
- Speicherung in SQLite-Datenbank inkl. SQL-Query
- Interaktive Streamlit-Web-App
- Optionale Analyse im Jupyter Notebook

---

## Projekt starten

### 1. Repository klonen (falls noch nicht geschehen)

### 2. `.env`-Datei erstellen mit deinem API-Zugang

Inhalt der Datei `.env`:

TRAVELPAYOUTS_TOKEN=dein_token_hier

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


